# Lab 16: Capstone Lab: Designing and Deploying a Complete Forensic Pipeline

**Course:** DFSP-5208  |  **Lecture week:** 16  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Integrate scripting, error handling, logging, containerization, and CI/CD from Labs 1–15 into one working pipeline.
- Design a pipeline that ingests raw log data, filters it, flags IOC matches, alerts via email, and archives results.
- Present and defend design decisions in a short demo to the class/instructor.

## Short theory

The capstone consolidates the semester's tools into one forensic evidence-processing pipeline end to end: a Bash orchestration script (Lab 5) runs a Python filtering script (Labs 2–3) with timestamped logging (Lab 12) and defensive error handling (Lab 11); the filtered data is scanned by the IOC function (Lab 8, through the local harness or faasd); the scan result is read by an alert script that e-mails through the SMTP sink (Lab 10); the results are archived with a SHA-256 hash; and the whole toolchain is containerized (Lab 13), pushed to the local registry (Lab 14), and built automatically by CI/CD (Lab 15). Every stage reads exactly what the previous stage wrote, and all components remain free and open source.

## Prerequisites

- Labs 1–15 completed and their artifacts available.
- The SMTP sink from Lab 10 running (Mailpit or aiosmtpd on port 1025).
- A short (5–10 minute) in-class or recorded demo slot booked with the instructor.

## Step-by-step solution


### Step 1: Design the pipeline

Sketch a diagram (hand-drawn, draw.io free tier, or the OSS tool Excalidraw) showing data flow: raw logs → filter script → IOC scan → alert → archive → CI/CD. Submit the diagram alongside the code.

### Step 2: Assemble the project repository

Copy the files from earlier labs. The Jenkinsfile and Dockerfile come from lab13 (that is where Lab 15 created them).

```bash
mkdir -p ~/forensic-scripting/capstone && cd ~/forensic-scripting/capstone
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

The pipeline needs data/raw.csv. Create it with this content:

```csv
timestamp,host,level,message
2026-03-04T10:00:00,host-1,INFO,user admin logged in
2026-03-04T10:01:00,host-2,ERROR,outbound connection to 203.0.113.99 flagged
2026-03-04T10:02:00,host-3,ERROR,disk almost full
2026-03-04T10:03:00,host-2,WARN,process malicious.exe started
```

> 📁 Saved as [`code/raw.csv`](code/raw.csv)


### Step 4: Write the alert script (it reads the scan result)

In the earlier draft the alert script ignored the scan result and used a hard-coded line, so the stages were not connected. This version reads the JSON written by the scan stage and e-mails only when it reports a match.

```python
import json, os, smtplib, sys
from email.mime.text import MIMEText

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    result = json.load(f)
result = result.get("body", result)            # accept the raw function body or the harness envelope
if not result.get("matched"):
    print("No IOC matches, no alert sent")
    sys.exit(0)

msg = MIMEText(f"IOC hits: {result['hits']}")
msg["Subject"] = "Forensic Alert: IOC Match"
msg["From"], msg["To"] = "soc-automation@lab.local", "analyst@lab.local"
host, port = os.getenv("MAIL_HOST", "localhost"), int(os.getenv("MAIL_PORT", "1025"))
try:
    with smtplib.SMTP(host, port, timeout=10) as server:
        server.send_message(msg)
except (OSError, smtplib.SMTPException) as exc:
    sys.exit(f"Alert failed: {exc}")
print("Alert sent:", result["hits"])
```

> 📁 Saved as [`code/step04_write-the-alert-script-it-reads-the-scan.py`](code/step04_write-the-alert-script-it-reads-the-scan.py)


### Step 5: Write the orchestration script

run_pipeline.sh stops at the first failure and logs every stage with a UTC timestamp. When SCAN_URL is set it calls the deployed function; otherwise it runs the same handler through the local harness.

```bash
#!/usr/bin/env bash
# Capstone orchestrator: stops at the first failure and logs each stage with a UTC timestamp.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data out
log() { echo "$(date -u +%FT%TZ) $*" | tee -a out/pipeline.log; }

log "[1/4] Filtering raw logs"
python3 scripts/log_filter_cli.py --input data/raw.csv --output data/filtered.csv --level ERROR

log "[2/4] Scanning for IOC matches"
if [ -n "${SCAN_URL:-}" ]; then                      # production: the faasd function, e.g. http://host.docker.internal:8080/function/ioc-alert
  curl -fsS -X POST "$SCAN_URL" --data-binary @data/filtered.csv > data/scan_result.json
else                                                 # no faasd available: run the same handler through the local harness
  node faas/harness.js faas/handler.js "$(cat data/filtered.csv)" > data/scan_result.json
fi

log "[3/4] Sending alert if matches found"
python3 scripts/alert_from_scan.py data/scan_result.json

log "[4/4] Archiving results"
ARCHIVE="out/archive_$(date -u +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$ARCHIVE" data/
sha256sum "$ARCHIVE" >> out/SHA256SUMS
log "Pipeline complete: $ARCHIVE"
```

> 📁 Saved as [`code/run_pipeline.sh`](code/run_pipeline.sh)


### Step 6: Run an end-to-end test and capture evidence


```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
cat data/scan_result.json
sha256sum -c out/SHA256SUMS
```

Expected output (times differ): four stages are logged, the filter writes 2 rows with level=ERROR, the alert script prints Alert sent: ['203.0.113.99'], and sha256sum reports the archive as OK.

```text
2026-10-09T10:53:38Z [1/4] Filtering raw logs
2 rows with level=ERROR written to data/filtered.csv (0 skipped)
2026-10-09T10:53:38Z [2/4] Scanning for IOC matches
2026-10-09T10:53:38Z [3/4] Sending alert if matches found
Alert sent: ['203.0.113.99']
2026-10-09T10:53:38Z [4/4] Archiving results
2026-10-09T10:53:38Z Pipeline complete: out/archive_20261009_105338.tar.gz
```


### Step 7: Containerise the pipeline

Inside a container 127.0.0.1 means the container itself, so the function and the mail server on the host are reached through host.docker.internal. The slim image has no curl, so it is installed, and the pipeline runs as a non-root user. Only the out folder is mounted.

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN useradd --create-home appuser && mkdir -p data out && chown -R appuser /app
USER appuser
ENTRYPOINT ["./run_pipeline.sh"]
```

> 📁 Saved as [`code/Dockerfile.step07`](code/Dockerfile.step07)


```bash
docker build -f docker/Dockerfile -t forensic-pipeline:1.0 .
docker run --rm --add-host=host.docker.internal:host-gateway \
  -e SCAN_URL=http://host.docker.internal:8080/function/ioc-alert \
  -e MAIL_HOST=host.docker.internal \
  -v "$PWD/out:/app/out" forensic-pipeline:1.0
```

Push the image to the local registry as forensic-pipeline:1.0 (docker tag, then docker push localhost:5000/forensic-pipeline:1.0).

### Step 8: Wire it into CI/CD

Reuse the Lab 15 pipeline with an added Deploy stage (Jenkins) or job (GitHub Actions) that builds the new pipeline image and runs it on every successful build.

### Step 9: Prepare the demo

Be ready to show: the pipeline diagram, a live or recorded run, the CI/CD build history, the alert e-mail in the SMTP sink, and your answer to “what happens if the scan stage fails?” (the script stops because of set -e).

## Required outcomes / tasks

- [ ] Complete capstone repository (scripts/, faas/, docker/, jenkins/, run_pipeline.sh, and the design diagram).
A successful end-to-end run log (or screen recording, system clock visible) from ingestion through to the archived output, its verified SHA-256, and the alert email.
- [ ] 5–10 minute live or recorded demo presented to the instructor, with a short Q&A on design trade-offs.
- [ ] One-page written reflection: which lab's tool was hardest to integrate, and how was the problem resolved?

## Code files in this lab

- [`code/Dockerfile.step07`](code/Dockerfile.step07)
- [`code/raw.csv`](code/raw.csv)
- [`code/run_pipeline.sh`](code/run_pipeline.sh)
- [`code/step04_write-the-alert-script-it-reads-the-scan.py`](code/step04_write-the-alert-script-it-reads-the-scan.py)
