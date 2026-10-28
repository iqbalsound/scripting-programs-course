# Lab 11: Error Handling and Debugging in Scripts

**Course:** DFSP-5208  |  **Lecture week:** 12  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Apply try/except (Python) and try/catch (Node.js) to handle predictable failure conditions.
- Use the free, built-in VS Code debugger to step through a script and inspect variables.
- Produce scripts that fail gracefully with clear error messages instead of crashing.

## Short theory

A forensic script that crashes mid-run on a single malformed log line can corrupt an entire evidence-processing job. Defensive coding, catching specific exceptions, validating input, and logging failures, is essential for reliability. VS Code's built-in debugger (free, no extension required for Python once the Python extension is installed) allows breakpoints, step-through execution, and live variable inspection without any paid tooling.

## Prerequisites

- Lab 2 and Lab 9 completed.
- VS Code with the Python extension installed.
- Git installed and a remote on GitHub or Gitea (free) for the pull-request task.

## Step-by-step solution


### Step 1: Create the messy data file

Create messy_log.csv with three deliberately malformed rows (a word, an empty value and a value with a stray letter).

```csv
timestamp,severity
2026-03-04T10:00:00,3
2026-03-04T10:01:00,high
2026-03-04T10:02:00,
2026-03-04T10:03:00,2
2026-03-04T10:04:00,9x
```

> 📁 Saved as [`code/messy_log.csv`](code/messy_log.csv)


### Step 2: Run a deliberately fragile script


```python
import csv

def parse_row(row):
    return {
        "timestamp": row["timestamp"],
        "severity": int(row["severity"]),   # will crash on non-numeric values
    }

with open("messy_log.csv") as f:
    for row in csv.DictReader(f):
        print(parse_row(row))
```

> 📁 Saved as [`code/parse_messy_fragile.py`](code/parse_messy_fragile.py)

Run it and read the traceback: it stops at the first bad row with a ValueError.

### Step 3: Add targeted exceptions, timestamped logging and a custom exception

Catch only the exceptions you expect (KeyError, ValueError, TypeError), never a bare except. Log with a timestamp so the log can be placed on a timeline. RetryExhausted is a custom exception raised when every attempt of a retried operation fails.

```python
import csv, logging, time

logging.basicConfig(filename="parse_errors.log", level=logging.WARNING,
                    format="%(asctime)s %(levelname)s %(message)s")


class RetryExhausted(Exception):
    """Raised when every attempt of a retried operation has failed."""


def parse_row(row):
    try:
        return {"timestamp": row["timestamp"], "severity": int(row["severity"])}
    except (KeyError, ValueError, TypeError) as exc:
        logging.warning("Skipped malformed row %r: %s", row, exc)
        return None


def with_retry(fn, attempts=3, delay=1.0, retry_on=(OSError,)):
    """Retry fn on transient errors. requests' exceptions subclass OSError, NOT the builtin ConnectionError."""
    for i in range(1, attempts + 1):
        try:
            return fn()
        except retry_on as exc:
            logging.warning("Attempt %d/%d failed: %s", i, attempts, exc)
            time.sleep(delay * 2 ** (i - 1))
    raise RetryExhausted(f"all {attempts} attempts failed")


if __name__ == "__main__":
    results = []
    try:
        with open("messy_log.csv", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                parsed = parse_row(row)
                if parsed:
                    results.append(parsed)
    except FileNotFoundError:
        logging.error("messy_log.csv not found")
        raise SystemExit("messy_log.csv not found")
    print(f"Successfully parsed {len(results)} rows; see parse_errors.log for skipped rows")
```

> 📁 Saved as [`code/parse_messy.py`](code/parse_messy.py)

Expected: Successfully parsed 2 rows; see parse_errors.log for skipped rows. The log lines start with a date and time, for example 2026-10-09 10:53:38,467 WARNING Skipped malformed row ...

### Step 4: Demonstrate the custom exception

Add this to the end of the script (inside the if __name__ block or in a separate file) and run it: every attempt fails, the retries are logged, and RetryExhausted is raised and caught.

```python
def always_fails():
    raise OSError("simulated outage")

try:
    with_retry(always_fails, attempts=3, delay=0.1)
except RetryExhausted as exc:
    print("giving up:", exc)
```

> 📁 Saved as [`code/demo_custom_exception.py`](code/demo_custom_exception.py)


### Step 5: Debug with VS Code and with pdb

In VS Code, click to the left of the `return` line inside parse_row to set a breakpoint, press F5 (Run ▸ Start Debugging), open the Variables panel and step with F10. When the value of the bad field is visible, take your screenshot.
The same job in the terminal needs no editor: b parse_row sets a breakpoint, c continues, p row prints the row, n steps to the next line.

```bash
python3 -m pdb parse_messy.py
(Pdb) b parse_row
(Pdb) c
(Pdb) p row
(Pdb) n
(Pdb) c
```


### Step 6: Node.js equivalent

In Node.js the same defensive pattern uses a check (or try/catch) and a timestamped warning:

```javascript
function parseRow(row) {
  const sev = Number(row.severity);
  if (row.severity === '' || Number.isNaN(sev)) {
    console.warn(`${new Date().toISOString()} WARN skipped row: invalid severity "${row.severity}"`);
    return null;
  }
  return { timestamp: row.timestamp, severity: sev };
}
```

> 📁 Saved as [`code/parse_messy.js`](code/parse_messy.js)

Add a few lines to run it over messy_log.csv:

```javascript
const fs = require('fs');
const [, ...lines] = fs.readFileSync('messy_log.csv', 'utf8').trim().split('\n');
const rows = lines.map(l => { const [timestamp, severity] = l.split(','); return { timestamp, severity }; });
const parsed = rows.map(parseRow).filter(Boolean); console.log(`Successfully parsed ${parsed.length} rows`);
```

> 📁 Saved as [`code/parse_messy_v2.js`](code/parse_messy_v2.js)


### Step 7: Review your change through a pull request

Commit the corrected script on a branch, push it, open a pull request and ask a classmate to review it. Reviewers check that no bare except remains and that every skipped row is logged.

```bash
cd ~/forensic-scripting/lab11
git init
git add parse_messy.py messy_log.csv
git commit -m "Lab 11: tolerant parser"
git switch -c feature/tolerant-parser
# push the branch and open the pull request on GitHub or Gitea
```


## Required outcomes / tasks

- [ ] messy_log.csv (with at least 3 deliberately malformed rows) and the corrected script submitted.
- [ ] parse_errors.log showing timestamped lines for the malformed rows being caught, not crashing the program.
- [ ] Screenshot of the VS Code debugger paused at a breakpoint with the Variables panel visible, or a pdb transcript showing `p` row, with the system clock visible.
- [ ] Screenshot of the RetryExhausted demonstration, and the link to your reviewed pull request.
- [ ] Two sentences: why is `except (KeyError, ValueError)` better than a bare except?

## Code files in this lab

- [`code/demo_custom_exception.py`](code/demo_custom_exception.py)
- [`code/messy_log.csv`](code/messy_log.csv)
- [`code/parse_messy.js`](code/parse_messy.js)
- [`code/parse_messy.py`](code/parse_messy.py)
- [`code/parse_messy_fragile.py`](code/parse_messy_fragile.py)
- [`code/parse_messy_v2.js`](code/parse_messy_v2.js)
