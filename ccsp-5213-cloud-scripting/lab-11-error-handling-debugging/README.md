# Lab 11: Error Handling and Debugging in Scripts

**Course:** CCSP-5213  |  **Lecture week:** 12  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Apply try/except (Python) and try/catch (Node.js) to handle predictable cloud API failures.
- Use the free, built-in VS Code debugger to step through a script and inspect variables.
- Produce scripts that fail gracefully instead of crashing an automation pipeline.

## Short theory

A cloud automation script that crashes on one malformed API response can halt an entire deployment pipeline. Defensive coding, catching specific exceptions, validating responses, retrying transient failures, is essential. VS Code's built-in debugger (free) allows breakpoints and live variable inspection at no cost, the same workflow used to debug production cloud automation code.

## Prerequisites

- Lab 2 and Lab 9 completed.
- VS Code with the Python extension installed.
- Git installed and a remote on GitHub or Gitea (free) for the pull-request task.

## Step-by-step solution


### Step 1: Create the messy data file

Create messy_billing.csv with three deliberately malformed rows (a word, an empty value and a value with a stray letter).

```csv
resource,cost
vm-01,72.5
db-02,abc
vm-03,
cache-04,19.99
vm-05,12x
```

> 📁 Saved as [`code/messy_billing.csv`](code/messy_billing.csv)


### Step 2: Run a deliberately fragile script


```python
import csv

def parse_row(row):
    return {"resource": row["resource"], "cost": float(row["cost"])}
# crashes on non-numeric cost

with open("messy_billing.csv") as f:
    for row in csv.DictReader(f):
        print(parse_row(row))
```

> 📁 Saved as [`code/parse_messy_fragile.py`](code/parse_messy_fragile.py)

Run it and read the traceback: it stops at the first bad row with a ValueError.

### Step 3: Add targeted exceptions, timestamped logging and a custom exception

Catch only the exceptions you expect (KeyError, ValueError, TypeError), never a bare except. Log with a timestamp so the log can be placed on a timeline. RetryExhausted is a custom exception raised when every attempt of a retried operation fails. The retry helper catches OSError, because the exceptions of the requests library derive from OSError, not from the built-in ConnectionError.

```python
import csv, logging, time

logging.basicConfig(filename="parse_errors.log", level=logging.WARNING,
                    format="%(asctime)s %(levelname)s %(message)s")


class RetryExhausted(Exception):
    """Raised when every attempt of a retried operation has failed."""


def parse_row(row):
    try:
        return {"resource": row["resource"], "cost": float(row["cost"])}
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
        with open("messy_billing.csv", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                parsed = parse_row(row)
                if parsed:
                    results.append(parsed)
    except FileNotFoundError:
        logging.error("messy_billing.csv not found")
        raise SystemExit("messy_billing.csv not found")
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

Cloud track: prove why the retry helper must not catch the built-in ConnectionError, then retry a real request correctly.

```bash
python3 -c "import requests; print(issubclass(requests.exceptions.ConnectionError, ConnectionError))"   # False
```


```python
import requests
with_retry(lambda: requests.get("http://127.0.0.1:1", timeout=5).raise_for_status(),
           attempts=2, delay=0.1, retry_on=(requests.exceptions.RequestException,))
```

> 📁 Saved as [`code/demo_custom_exception_v2.py`](code/demo_custom_exception_v2.py)


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
  const cost = Number(row.cost);
  if (row.cost === '' || Number.isNaN(cost)) {
    console.warn(`${new Date().toISOString()} WARN skipped row: invalid cost "${row.cost}"`);
    return null;
  }
  return { resource: row.resource, cost };
}
```

> 📁 Saved as [`code/parse_messy.js`](code/parse_messy.js)

Add a few lines to run it over messy_billing.csv:

```javascript
const fs = require('fs');
const [, ...lines] = fs.readFileSync('messy_billing.csv', 'utf8').trim().split('\n');
const rows = lines.map(l => { const [resource, cost] = l.split(','); return { resource, cost }; });
const parsed = rows.map(parseRow).filter(Boolean); console.log(`Successfully parsed ${parsed.length} rows`);
```

> 📁 Saved as [`code/parse_messy_v2.js`](code/parse_messy_v2.js)


### Step 7: Review your change through a pull request

Commit the corrected script on a branch, push it, open a pull request and ask a classmate to review it. Reviewers check that no bare except remains and that every skipped row is logged.

```bash
cd ~/cloud-scripting/lab11
git init
git add parse_messy.py messy_billing.csv
git commit -m "Lab 11: tolerant parser"
git switch -c feature/tolerant-parser
# push the branch and open the pull request on GitHub or Gitea
```


## Required outcomes / tasks

- [ ] messy_billing.csv (with at least 3 deliberately malformed rows) and the corrected script submitted.
- [ ] parse_errors.log showing timestamped lines for the malformed rows being caught, not crashing the program.
- [ ] Screenshot of the VS Code debugger paused at a breakpoint with the Variables panel visible, or a pdb transcript showing `p` row, with the system clock visible.
- [ ] Screenshot of the RetryExhausted demonstration, and the link to your reviewed pull request.
- [ ] Two sentences: why is `except (KeyError, ValueError)` better than a bare except?

## Code files in this lab

- [`code/demo_custom_exception.py`](code/demo_custom_exception.py)
- [`code/demo_custom_exception_v2.py`](code/demo_custom_exception_v2.py)
- [`code/messy_billing.csv`](code/messy_billing.csv)
- [`code/parse_messy.js`](code/parse_messy.js)
- [`code/parse_messy.py`](code/parse_messy.py)
- [`code/parse_messy_fragile.py`](code/parse_messy_fragile.py)
- [`code/parse_messy_v2.js`](code/parse_messy_v2.js)
