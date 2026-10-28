# Lab 16: Capstone Lab: Designing and Deploying a Complete Cloud-Native Application

**Course:** CCSP-5213  |  **Lecture week:** 16  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Integrate scripting, error handling, logging, containerization, storage, and CI/CD from Labs 1–15 into one pipeline.
- Design a pipeline that ingests usage data, checks budgets, stores artefacts in MinIO, alerts via email, and deploys automatically.
- Present and defend design decisions in a short demo to the class/instructor.

## Short theory

The capstone consolidates the semester's tools into one cloud-native pipeline end to end: a Bash orchestration script (Lab 5) runs a Python filtering script (Labs 2–3) with timestamped logging (Lab 12) and defensive error handling (Lab 11); each filtered usage row is converted to JSON and sent to the usage-alert function (Lab 8, through the local harness or faasd); the answers are read by an alert script that e-mails through the SMTP sink (Lab 10); the results are archived with a SHA-256 hash and uploaded to the S3 emulator (Lab 14); and the whole toolchain is containerised (Lab 13), pushed to the local registry (Lab 14), and built automatically by CI/CD (Lab 15). Every stage reads exactly what the previous stage wrote, and all components remain free and open source.

## Prerequisites

- Labs 1–15 completed and their artifacts available.
- The SMTP sink from Lab 10 running (Mailpit or aiosmtpd on port 1025) and the Moto server from Lab 14 running (optional, for the upload stage).
- A short (5–10 minute) in-class or recorded demo slot booked with the instructor.

## Step-by-step solution


### Step 1: Design the pipeline

Sketch a diagram (hand-drawn, draw.io free tier, or the OSS tool Excalidraw) showing data flow: usage data → filter script → budget check (JSON per row) → alert → archive and upload → CI/CD. Submit the diagram alongside the code.

### Step 2: Assemble the project repository

Copy the files from earlier labs. The Jenkinsfile and Dockerfile come from lab13 (that is where Lab 15 created them).

```bash
mkdir -p ~/cloud-scripting/capstone && cd ~/cloud-scripting/capstone
git init
mkdir -p data scripts faas docker jenkins .github/workflows out
cp ../lab03/log_filter_cli.py scripts/
cp ../lab08/handler.js ../lab08/harness.js faas/
cp ../lab13/Dockerfile docker/Dockerfile.lab13
cp ../lab13/Jenkinsfile jenkins/
cp ../lab13/.github/workflows/ci.yml .github/workflows/ 2>/dev/null || true   # only if you completed Route B
```

Target layout:

```text
capstone/
  data/raw.csv
  scripts/log_filter_cli.py     (Lab 3)
  scripts/alert_from_scan.py
  faas/handler.js  faas/harness.js   (Lab 8)
  docker/Dockerfile   jenkins/Jenkinsfile   .github/workflows/ci.yml
  run_pipeline.sh   diagram.png   README.md
```


### Step 3: Supply the input data

The pipeline needs data/usage.csv, including one deliberately invalid row.

```csv
resource,costUsd,level
vm-01,72.5,WARN
db-02,20.0,INFO
vm-03,130.0,WARN
bad-row,abc,WARN
```

> 📁 Saved as [`code/usage.csv`](code/usage.csv)


### Step 4: Write the budget-check script

The earlier draft posted a CSV to a function that calls JSON.parse, which throws. This script converts each row to JSON and calls the function once per row; an invalid row is rejected but does not stop the run. With SCAN_URL unset it uses the local harness.

```python
"""Send each filtered usage row to the usage-alert function and collect the answers."""
import csv, json, os, subprocess, sys, urllib.request

src, dst = sys.argv[1], sys.argv[2]
url = os.getenv("SCAN_URL")                      # e.g. http://host.docker.internal:8080/function/usage-alert
results = []
with open(src, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        payload = json.dumps({"resource": row["resource"], "costUsd": row["costUsd"]})
        if url:
            req = urllib.request.Request(url, data=payload.encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                results.append(json.load(r))
        else:
            out = subprocess.run(["node", "faas/harness.js", "faas/handler.js", payload], capture_output=True, text=True, check=True)
            results.append(json.loads(out.stdout)["body"])
with open(dst, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
errors = [r for r in results if "error" in r]
over = [r for r in results if r.get("overBudget")]
print(f"{len(results) - len(errors)} resources checked, {len(errors)} rejected as invalid, {len(over)} over budget: {[r['resource'] for r in over]}")
```

> 📁 Saved as [`code/step04_write-the-budget-check-script.py`](code/step04_write-the-budget-check-script.py)


### Step 5: Write the alert and upload scripts

alert_from_scan.py reads the budget-check result and e-mails the resources over budget. upload_to_s3.py sends the archive to the S3 emulator.

```python
import json, os, smtplib, sys
from email.mime.text import MIMEText

with open(sys.argv[1], encoding="utf-8") as f:
    results = json.load(f)
over = [r for r in results if r.get("overBudget")]
if not over:
    print("Within budget, no alert sent")
    sys.exit(0)

msg = MIMEText("Resources over budget:\n" + "\n".join(f"-{r['resource']}: ${r['costUsd']:.2f}" for r in over))
msg["Subject"] = f"Cloud Cost Alert: {len(over)} resource(s) over budget"
msg["From"], msg["To"] = "cost-automation@lab.local", "ops@lab.local"
try:
    with smtplib.SMTP(os.getenv("MAIL_HOST", "localhost"), int(os.getenv("MAIL_PORT", "1025")), timeout=10) as s:
        s.send_message(msg)
except (OSError, smtplib.SMTPException) as exc:
    sys.exit(f"Alert failed: {exc}")
print("Alert sent for:", [r["resource"] for r in over])
```

> 📁 Saved as [`code/alert_from_scan.py`](code/alert_from_scan.py)


```python
import os, sys, boto3
s3 = boto3.client("s3", endpoint_url=os.getenv("S3_URL", "http://localhost:5000"), region_name="us-east-1",
                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),

aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"))
bucket, path = "pipeline-artifacts", sys.argv[1]
try:
    s3.create_bucket(Bucket=bucket)
except s3.exceptions.BucketAlreadyOwnedByYou:
    pass
s3.upload_file(path, bucket, os.path.basename(path))
print("uploaded", path, "to", bucket)
```

> 📁 Saved as [`code/step05_alert_from_scan.py`](code/step05_alert_from_scan.py)


### Step 6: Write the orchestration script and run it


```bash
#!/usr/bin/env bash
# Cloud capstone orchestrator: stops at the first failure; logs each stage with a UTC timestamp.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data out
log() { echo "$(date -u +%FT%TZ) $*" | tee -a out/pipeline.log; }

log "[1/5] Filtering usage data"
python3 scripts/log_filter_cli.py --input data/usage.csv --output data/filtered.csv --level WARN
log "[2/5] Checking budgets"
python3 scripts/check_budgets.py data/filtered.csv data/scan_result.json
log "[3/5] Alerting if over budget"
python3 scripts/alert_from_scan.py data/scan_result.json
ARCHIVE="out/archive_$(date -u +%Y%m%d_%H%M%S).tar.gz"
log "[4/5] Archiving"
tar -czf "$ARCHIVE" data/
sha256sum "$ARCHIVE" >> out/SHA256SUMS
if [ -n "${S3_URL:-}" ]; then                         # skipped when no S3 endpoint is configured
  log "[5/5] Uploading to the S3 endpoint"
  python3 scripts/upload_to_s3.py "$ARCHIVE"
fi
log "Pipeline complete: $ARCHIVE"
```

> 📁 Saved as [`code/step06_write-the-orchestration-script-and-run-i.sh`](code/step06_write-the-orchestration-script-and-run-i.sh)


```bash
chmod +x run_pipeline.sh
THRESHOLD_USD=50 ./run_pipeline.sh                        # upload stage skipped
S3_URL=http://localhost:5000 THRESHOLD_USD=50 ./run_pipeline.sh   # with Moto running
sha256sum -c out/SHA256SUMS
```

Expected: 3 rows are filtered, 2 resources are checked and 1 is rejected as invalid, vm-01 and vm-03 are over a 50 threshold, an alert e-mail is sent, and the archive appears in the bucket listing when S3_URL is set.

### Step 7: Containerise the pipeline

Inside a container 127.0.0.1 means the container itself, so the function and the mail server on the host are reached through host.docker.internal. The image needs boto3 for the upload stage and runs as a non-root user. Only the out folder is mounted.

```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir boto3
WORKDIR /app
COPY . .
RUN useradd --create-home appuser && mkdir -p data out && chown -R appuser /app
USER appuser
ENTRYPOINT ["./run_pipeline.sh"]
```

> 📁 Saved as [`code/Dockerfile.step07`](code/Dockerfile.step07)


```bash
docker build -f docker/Dockerfile -t cloud-pipeline:1.0 .
docker run --rm --add-host=host.docker.internal:host-gateway \
  -e SCAN_URL=http://host.docker.internal:8080/function/usage-alert \
  -e MAIL_HOST=host.docker.internal \
  -e S3_URL=http://host.docker.internal:5000 \
  -v "$PWD/out:/app/out" cloud-pipeline:1.0
```

Push the image to the local registry as cloud-pipeline:1.0 (docker tag, then docker push localhost:5000/cloud-pipeline:1.0).

### Step 8: Wire it into CI/CD

Reuse the Lab 15 pipeline with an added Deploy stage (Jenkins) or job (GitHub Actions) that builds the new pipeline image and runs it on every successful build.

### Step 9: Prepare the demo

Be ready to show: the pipeline diagram, a live or recorded run, the CI/CD build history, the alert e-mail in the SMTP sink, the archive in the S3 bucket listing, and your answer to “what happens if the function is down?”.

## Required outcomes / tasks

- [ ] Complete capstone repository (scripts/, faas/, docker/, jenkins/, run_pipeline.sh, and the design diagram).
- [ ] A successful end-to-end run log (or screen recording, system clock visible) from ingestion through to the archived output, its verified SHA-256, and the alert email.
- [ ] 5–10 minute live or recorded demo presented to the instructor, with a short Q&A on design trade-offs.
- [ ] One-page written reflection: which lab's tool was hardest to integrate, and how was the problem resolved?

## Code files in this lab

- [`code/Dockerfile.step07`](code/Dockerfile.step07)
- [`code/alert_from_scan.py`](code/alert_from_scan.py)
- [`code/step04_write-the-budget-check-script.py`](code/step04_write-the-budget-check-script.py)
- [`code/step05_alert_from_scan.py`](code/step05_alert_from_scan.py)
- [`code/step06_write-the-orchestration-script-and-run-i.sh`](code/step06_write-the-orchestration-script-and-run-i.sh)
- [`code/usage.csv`](code/usage.csv)
