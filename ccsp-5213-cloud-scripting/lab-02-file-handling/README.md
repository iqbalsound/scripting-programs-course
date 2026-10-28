# Lab 2: File Handling and Automation in Python

**Course:** CCSP-5213  |  **Lecture week:** 2  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Read, write, and append text and CSV files using Python's standard library only.
- Automate a repetitive cloud data-processing task without manual copy-pasting.
- Apply context managers (with) to guarantee files are closed safely.

## Short theory

Most real cloud automation tasks begin and end with a file: a log dump, a CSV export, or a folder of evidence files that must be renamed or summarized. Python's built-in open(), the `csv` module, and the `pathlib` module (all part of the free standard library, no extra installation needed) are sufficient for the overwhelming majority of file-handling tasks and are the foundation for the log-parsing and API labs later in the course.
Programs also fail: a file may be missing or a row malformed. A try/except block lets a script report the problem clearly instead of crashing; this lab uses it once, and Lab 11 develops the idea fully.

## Prerequisites

- Lab 1 completed (Python 3.12 or newer + venv working).
- A sample CSV file (students may generate one with the script in Step 2 if none is supplied).

## Step-by-step solution


### Step 1: Activate the environment and create a working folder


```bash
cd ~/cloud-scripting
mkdir lab02 && cd lab02
source ../lab01/.venv/bin/activate
```


### Step 2: Generate a sample dataset

Create generate_sample.py to produce a synthetic cloud billing/usage dataset for practice (no real/sensitive data is used). The fixed random seed means every student gets the same data, so results can be checked: with seed 42 you should see 12 ERROR, 16 WARN and 22 INFO rows.

```python
import csv, random, datetime

random.seed(42)                      # same data on every run, so answers can be checked
now = datetime.datetime.now(datetime.timezone.utc)
rows = []
for i in range(50):
    ts = now - datetime.timedelta(minutes=i * 7)
    rows.append([ts.isoformat(timespec="seconds"), f"host-{random.randint(1, 5)}",
                 random.choice(["INFO", "WARN", "ERROR"]), f"event id {i}"])
with open("sample_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "host", "level", "message"])
    writer.writerows(rows)
print("sample_data.csv generated")
```

> 📁 Saved as [`code/generate_sample.py`](code/generate_sample.py)


### Step 3: Generate the resource inventory used by Assignment 1

Cloud work also starts from inventories. Create generate_resources.py to produce resources.csv with the columns id, region and status.

```python
import csv, random

random.seed(42)
regions = ["us-east-1", "eu-west-1", "ap-south-1"]
statuses = ["running", "stopped", "degraded"]
with open("resources.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "region", "status"])
    for i in range(1, 31):
        writer.writerow([f"res-{i:03d}", random.choice(regions), random.choice(statuses)])
print("resources.csv generated")
```

> 📁 Saved as [`code/generate_resources.py`](code/generate_resources.py)


### Step 4: Read, filter and count the file

Write filter_errors.py to extract only ERROR-level rows using the csv module and pathlib, count every level, and append a UTC run-log entry (append, not overwrite) each time the script executes.

```python
import csv, datetime
from pathlib import Path

src, dst = Path("sample_data.csv"), Path("errors_only.csv")
counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
with src.open(newline="", encoding="utf-8") as inp, dst.open("w", newline="", encoding="utf-8") as out:
    reader = csv.DictReader(inp)
    writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        counts[row["level"]] = counts.get(row["level"], 0) + 1
        if row["level"] == "ERROR":
            writer.writerow(row)
print(f"{counts['ERROR']} ERROR rows written to {dst}; {counts['WARN']} WARN rows seen; {counts['INFO']} INFO rows seen")

with open("run_history.log", "a", encoding="utf-8") as log:
    log.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')} - filter_errors.py executed\n")
```

> 📁 Saved as [`code/filter_errors.py`](code/filter_errors.py)


### Step 5: Handle a missing file (exception primer)

Wrap a risky step in try/except and exit with a clear message instead of a traceback.

```python
from pathlib import Path

src = Path("sample_data.csv")
try:
    text = src.read_text(encoding="utf-8")
except FileNotFoundError:
    raise SystemExit(f"Input file not found: {src}")
print(f"{len(text.splitlines())} lines read from {src}")
```

> 📁 Saved as [`code/step05_handle-a-missing-file-exception-primer.py`](code/step05_handle-a-missing-file-exception-primer.py)


### Step 6: Execute and verify


```bash
python generate_sample.py
python filter_errors.py
head errors_only.csv
cat run_history.log
```


## Required outcomes / tasks

- [ ] sample_data.csv, errors_only.csv, and run_history.log submitted together, with a screenshot of the run (system clock visible).
- [ ] resources.csv generated with generate_resources.py (30 rows; id, region, status).
Extend filter_errors.py so it also writes warn_only.csv and prints the percentage of rows at each level; submit the modified script.
- [ ] Explain in 2–3 sentences why `with open(...)` is preferred over calling open()/close() manually.

## Code files in this lab

- [`code/filter_errors.py`](code/filter_errors.py)
- [`code/generate_resources.py`](code/generate_resources.py)
- [`code/generate_sample.py`](code/generate_sample.py)
- [`code/step05_handle-a-missing-file-exception-primer.py`](code/step05_handle-a-missing-file-exception-primer.py)
