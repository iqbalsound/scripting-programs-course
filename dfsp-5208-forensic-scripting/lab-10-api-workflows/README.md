# Lab 10: Automating Security Workflows with APIs

**Course:** DFSP-5208  |  **Lecture week:** 11  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Chain a file-scan step with an automated email alert using only free, open-source components.
- Use a local SMTP test server (Mailpit, or Python's aiosmtpd) as the mail sink, with no real mail credentials required.
- Make the workflow safe to schedule: remember what was already alerted in SQLite so the same finding is never e-mailed twice.

## Short theory

Security workflows typically end with a notification. Rather than requiring a paid SMTP relay or real inbox credentials, a local SMTP sink captures every message: Mailpit shows them in a web UI, and Python's aiosmtpd prints them in the terminal. (MailHog, used in earlier editions, has had no release since 2020.) This lab connects the IOC-detection logic from Lab 8 to an automated alert email, the same pattern used in real Security Orchestration, Automation and Response (SOAR) pipelines. Two habits make such a workflow production-ready: send one consolidated message instead of one per finding, and keep state (here in SQLite) so that a scheduled job does not repeat itself.

## Prerequisites

- Lab 8 completed (Tier 1 handler tested).
- Lab 9 completed (requests/fetch).
- Docker (installed in Lab 1) for Mailpit, or `pip install aiosmtpd` if Docker is not available.

## Step-by-step solution


### Step 1: Start a local SMTP sink (free, OSS)

Option A: Mailpit in Docker. Option B: Python's aiosmtpd, which prints each message in the terminal. Both listen on port 1025.

```bash
cd ~/forensic-scripting && mkdir lab10 && cd lab10
# Option A: Mailpit (web UI at http://localhost:8025)
docker run -d --name mailpit -p 1025:1025 -p 8025:8025 axllent/mailpit

# Option B: aiosmtpd (messages are printed in this terminal)
source ../lab01/.venv/bin/activate
pip install aiosmtpd
python -m aiosmtpd -n -l localhost:1025
```


### Step 2: Write the alert workflow in Python

The script scans first, collects every match, and sends one consolidated email. If nothing matches it sends nothing; if the SMTP server is down it exits with a clear message.

```python
import smtplib, sys
from email.mime.text import MIMEText

SMTP_HOST, SMTP_PORT = "localhost", 1025
IOCS = ["malicious.exe", "203.0.113.99"]
LOG_LINES = [
    "user admin logged in from 10.0.0.5",
    "outbound connection to 203.0.113.99 flagged",
    "process malicious.exe started by user bob",
    "scheduled backup completed",
    "dns query for example.org",
]


def scan_line(line):
    return [i for i in IOCS if i in line]


def send_summary(findings):
    body = "IOC summary\n" + "\n".join(f"- line {n}: {hits} -> {line}" for n, hits, line in findings)
    msg = MIMEText(body)
    msg["Subject"] = f"Forensic Alert: {len(findings)} IOC match(es)"
    msg["From"], msg["To"] = "soc-automation@lab.local", "analyst@lab.local"
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        server.send_message(msg)


if __name__ == "__main__":
    findings = [(n, h, l) for n, l in enumerate(LOG_LINES, 1) if (h := scan_line(l))]
    if not findings:
        print("No IOC matches, no alert sent")
        sys.exit(0)
    try:
        send_summary(findings)                                  # ONE consolidated email, not one per line
    except (OSError, smtplib.SMTPException) as exc:
        sys.exit(f"Alert failed: {exc}")
    print(f"Consolidated alert sent: {len(findings)} matches in {len(LOG_LINES)} lines")
```

> 📁 Saved as [`code/alert_workflow.py`](code/alert_workflow.py)


### Step 3: Run the workflow and check the sink


```bash
python alert_workflow.py
# Mailpit: open http://localhost:8025 in a browser to view the captured email
# aiosmtpd: the message appears in the terminal where it is running
```

Expected: one email listing every match, not one email per line.

### Step 4: Node.js equivalent using nodemailer (free, OSS)


```bash
npm install nodemailer
```


### Step 5: Write alert_workflow.js


```javascript
const nodemailer = require('nodemailer');
const IOCS = ['malicious.exe', '203.0.113.99'];
const LINES = ['user admin logged in', 'outbound connection to 203.0.113.99 flagged', 'process malicious.exe started', 'backup done', 'dns query'];

async function main() {
  const findings = LINES.map((l, i) => ({ n: i + 1, l, hits: IOCS.filter(x => l.includes(x)) })).filter(f => f.hits.length);
  if (!findings.length) return console.log('No IOC matches, no alert sent');
  const transporter = nodemailer.createTransport({ host: 'localhost', port: 1025, secure: false });
  await transporter.sendMail({
    from: 'soc-automation@lab.local', to: 'analyst@lab.local',
    subject: `Forensic Alert: ${findings.length} IOC match(es)`,
    text: findings.map(f => `- line ${f.n}: ${f.hits.join(', ')} -> ${f.l}`).join('\n'),
  });
  console.log(`Consolidated alert sent: ${findings.length} matches`); }
main().catch(e => { console.error('Alert failed:', e.message); process.exit(1); });
```

> 📁 Saved as [`code/alert_workflow.js`](code/alert_workflow.js)


### Step 6: Add state and a schedule

A scheduled workflow must not repeat itself. Keep an alerts table in SQLite and skip any entity that was alerted in the last 24 hours. Add the check before sending and an INSERT after a successful send, then schedule the script with cron.

```python
import sqlite3, datetime
conn = sqlite3.connect("alerts.db")
conn.execute("CREATE TABLE IF NOT EXISTS alerts (entity TEXT, ts TEXT, action TEXT)")
def already_alerted(entity, hours=24):
    cutoff = (datetime.datetime.now(datetime.timezone.utc) -datetime.timedelta(hours=hours)).isoformat()
    return conn.execute("SELECT 1 FROM alerts WHERE entity=? AND ts>? LIMIT 1", (entity, cutoff)).fetchone() is not None
# after a successful send: conn.execute("INSERT INTO alerts VALUES (?,?,?)", (entity, now_iso, "email")); conn.commit()
```

> 📁 Saved as [`code/alert_workflow_stateful.py`](code/alert_workflow_stateful.py)


```bash
crontab -e
# add:
*/30 * * * * cd $HOME/forensic-scripting/lab10 && $HOME/forensic-scripting/lab01/.venv/bin/python alert_workflow.py >> alert.out 2>&1
```

Run the script twice by hand first: the second run must report that the finding was already alerted and send no second email.

## Required outcomes / tasks

- [ ] Screenshot of the mail sink (Mailpit web UI or aiosmtpd terminal) showing one consolidated alert email, system clock visible.
- [ ] Both alert_workflow.py and alert_workflow.js submitted.
- [ ] Extend either script to loop over 5 sample log lines and send one consolidated summary email instead of one per line (the provided script already does this; show it with your own five lines and your own IOC).
- [ ] Output of `SELECT * FROM alerts;` after the state extension, and a second run that sends no email.

## Code files in this lab

- [`code/alert_workflow.js`](code/alert_workflow.js)
- [`code/alert_workflow.py`](code/alert_workflow.py)
- [`code/alert_workflow_stateful.py`](code/alert_workflow_stateful.py)
