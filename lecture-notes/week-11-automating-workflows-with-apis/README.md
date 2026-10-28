# Week 11: Automating Workflows with APIs

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 2 (Create) | ATBS (2nd ed.) Ch. 17-18 (scheduling, email); Python sqlite3 and smtplib docs | Fetch, evaluate, alert; SQLite state; scheduler |

> Revised for Fall 2026 Reading changed: Ch. 14 is Google Sheets in the 2nd edition; verify numbering for your edition. Primary alert channel is a free webhook (Discord/Slack). A local aiosmtpd debug SMTP server gives an offline email demonstration. The standard-library smtpd module was removed in Python 3.12. Windows students use Task Scheduler instead of cron (see Section 3).


### Learning objectives

- Chain API calls into a fetch-parse-evaluate-act workflow.
- Write small, testable functions with defensive validation.
- Persist state in SQLite to prevent duplicate alerts.
- Run the workflow unattended with a system scheduler and reason about idempotency.


### Hour 1: From single script to workflow

- A script answers one question once; a workflow decides and acts repeatedly. This synthesis is the "Create" level (CLO 2).
- Shape: fetch, parse, evaluate, act. Keep each stage a function so each can be tested alone.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Use case: alert the team when a monitored IP's abuse confidence rises above a threshold since the last check.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Use case: alert when a storage bucket's object count or a queue backlog crosses a threshold.


### Hour 2: Building the multi-step automation

- `fetch_data()` (reuse Week 10), `evaluate(data)` returns True/False after validating that the field exists and is numeric, `send_alert(text)` performs the action.
- Alert channels: webhook POST with `requests` (preferred); email with `smtplib` and an app password; or a local `aiosmtpd` server for demonstration.
- Never assume the field exists: a malformed response must not crash an unattended job overnight.

```python
import os, sqlite3, datetime, logging, requests
THRESHOLD = int(os.getenv("THRESHOLD", "50"))

def evaluate(data):
    try:
        score = data["data"]["abuseConfidenceScore"]
    except (KeyError, TypeError) as e:
        raise ValueError(f"missing field: {e}") from e
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise ValueError(f"score not numeric: {score!r}")
    return score > THRESHOLD

def send_alert(text):
    r = requests.post(os.environ["WEBHOOK_URL"], json={"content": text}, timeout=10)
    r.raise_for_status()
```

> 📁 Saved as [`code/example_01.py`](code/example_01.py)


### Hour 3: State persistence and unattended scheduling

- SQLite (built in) stores what has already been alerted on: entity, timestamp, action.
- Check the table before alerting; insert a row **only after** a successful send.
- Schedule with cron (`*/30 * * * *`) or Task Scheduler. Use absolute paths and log to a file; cron has a minimal environment.
- **Idempotency:** running twice for the same underlying data must produce one alert, not two.

```python
def already_alerted(conn, entity, hours=24):
    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)).isoformat()
    return conn.execute("SELECT 1 FROM alerts WHERE entity=? AND ts>? LIMIT 1", (entity, cutoff)).fetchone() is not None

conn = sqlite3.connect("alerts.db")
conn.execute("CREATE TABLE IF NOT EXISTS alerts (entity TEXT, ts TEXT, action TEXT)")
# ... after a successful send_alert():
conn.execute("INSERT INTO alerts VALUES (?,?,?)", (entity, datetime.datetime.now(datetime.timezone.utc).isoformat(), "webhook"))
conn.commit()
```

> 📁 Saved as [`code/example_02.py`](code/example_02.py)

**Optional local email demo:** run `python -m aiosmtpd -n -l localhost:1025` in one terminal (it prints each message it receives), then send with `smtplib.SMTP("localhost", 1025)` from your script. No account is needed.


### Step-by-step lab method (free and open-source tools only)

**Tools:** Python 3.12+, `requests`, built-in `sqlite3`, a free Discord/Slack webhook (or `aiosmtpd`), cron or Task Scheduler. Cloud track: the Week 10 emulator is the data source.

1. Reuse `fetch_data()` from Week 10 as the retrieval stage.
1. Write `evaluate(data)` with validation and a configurable threshold (use your personal seed).
1. Create the SQLite database and `alerts` table.
1. Before alerting, check `already_alerted()` for this entity.
1. Write `send_alert()` using a webhook or local SMTP.
1. Wrap `main()` in `try/except` that logs a failure instead of crashing.
1. Insert a row into `alerts` only after a successful send.
1. Schedule: Linux `crontab -e` with `*/30 * * * * /usr/bin/python3 /path/to/workflow.py`; Windows Task Scheduler (repeat every 30 minutes).
1. After the first scheduled run, inspect the state: `sqlite3 alerts.db "SELECT * FROM alerts;"`.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalised, see the Appendix on personalisation.

1. Run the complete fetch-evaluate-act workflow and paste the exact terminal output of one pass, showing the sequence of function calls.
1. Trigger the True branch of `evaluate()` using live (or mock) data and show the exact alert message produced.
1. Query `alerts.db` after your first scheduled run and paste the exact rows.
1. Using your own table contents, explain how the stored state prevented a duplicate alert on the second run.
1. Show your crontab entry (or Task Scheduler screenshot) including the schedule expression.
1. Corrupt one field in a test JSON response and report the exact exception your validation caught.
1. Report the actual wall-clock time your scheduled job fired versus the configured time, and explain any drift.
1. Identify one point where duplicate side effects could still occur (for example, the alert is sent but the process dies before the `INSERT`) and describe the specific code change that closes the gap.

## Code files in this week

- [`code/example_01.py`](code/example_01.py)
- [`code/example_02.py`](code/example_02.py)
