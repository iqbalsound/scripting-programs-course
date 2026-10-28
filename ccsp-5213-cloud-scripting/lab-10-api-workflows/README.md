# Lab 10: Automating Workflows with APIs

**Course:** CCSP-5213  |  **Lecture week:** 11  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Chain a cloud-cost-check step with an automated email alert using only free, open-source components.
- Use a local SMTP test server (Mailpit, or Python's aiosmtpd) as the mail sink, with no real cloud mail service required.
- Make the workflow safe to schedule: remember what was already alerted in SQLite so the same resource is never e-mailed twice.

## Short theory

Cost-overrun alerting is one of the most common cloud-automation workflows. A local SMTP sink lets smtplib/nodemailer be practised safely without real credentials or a paid mail relay: Mailpit shows captured messages in a web UI, and Python's aiosmtpd prints them in the terminal. (MailHog, used in earlier editions, has had no release since 2020.) This lab applies the same threshold idea as the Lab 8 usage-alert function to a list of resources in Python, mirroring real cloud cost-management alerting, and adds state so a scheduled job does not repeat itself.

## Prerequisites

- Lab 8 completed (Tier 1 handler tested).
- Lab 9 completed (requests/fetch).
- Docker (installed in Lab 1) for Mailpit, or `pip install aiosmtpd` if Docker is not available.

## Step-by-step solution


### Step 1: Start a local SMTP sink (free, OSS)

Option A: Mailpit in Docker. Option B: Python's aiosmtpd, which prints each message in the terminal. Both listen on port 1025.

```bash
cd ~/cloud-scripting && mkdir lab10 && cd lab10
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
BUDGET_USD = 50
RESOURCES = [("vm-01", 72.5), ("db-02", 20.0), ("vm-03", 130.0), ("cache-04", 49.99), ("vm-05", 51.0)]

def over_budget(resources):
    return [(name, cost) for name, cost in resources if cost > BUDGET_USD]

def send_summary(findings):
    body = "Resources over budget\n" + "\n".join(f"- {name}: ${cost:.2f} (limit ${BUDGET_USD})" for name, cost in findings)
    msg = MIMEText(body)
    msg["Subject"] = f"Cloud Cost Alert: {len(findings)} resources over budget"
    msg["From"], msg["To"] = "cost-automation@lab.local", "ops@lab.local"
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        server.send_message(msg)

if __name__ == "__main__":
    findings = over_budget(RESOURCES)
    if not findings:
        print("Within budget, no alert sent")
        sys.exit(0)
    try:
        send_summary(findings)                      # ONE consolidated email, not one per resource
    except (OSError, smtplib.SMTPException) as exc:
        sys.exit(f"Alert failed: {exc}")
    print(f"Consolidated alert sent: {len(findings)} of {len(RESOURCES)} resources over budget")
```

> 📁 Saved as [`code/alert_workflow.py`](code/alert_workflow.py)


### Step 3: Run the workflow and check the sink


```bash
python alert_workflow.py
# Mailpit: open http://localhost:8025 in a browser to view the captured email
# aiosmtpd: the message appears in the terminal where it is running
```

Expected: one email listing vm-01, vm-03 and vm-05 (cost above 50), with the subject Cloud Cost Alert: 3 resources over budget.

### Step 4: Node.js equivalent using nodemailer (free, OSS)


```bash
npm install nodemailer
```


### Step 5: Write alert_workflow.js


```javascript
const nodemailer = require('nodemailer');
const BUDGET_USD = 50;
const RESOURCES = [['vm-01', 72.5], ['db-02', 20.0], ['vm-03', 130.0], ['cache-04', 49.99], ['vm-05', 51.0]];
async function main() {
  const over = RESOURCES.filter(([, cost]) => cost > BUDGET_USD);
  if (!over.length) return console.log('Within budget, no alert sent');
  const transporter = nodemailer.createTransport({ host: 'localhost', port: 1025, secure: false });
  await transporter.sendMail({
    from: 'cost-automation@lab.local', to: 'ops@lab.local',
    subject: `Cloud Cost Alert: ${over.length} resources over budget`,
    text: over.map(([name, cost]) => `- ${name}: $${cost.toFixed(2)} (limit $${BUDGET_USD})`).join('\n'),
  });
  console.log(`Consolidated alert sent: ${over.length} resources over budget`);
}
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
*/30 * * * * cd $HOME/cloud-scripting/lab10 && $HOME/cloud-scripting/lab01/.venv/bin/python alert_workflow.py >> alert.out 2>&1
```

Run the script twice by hand first: the second run must report that the finding was already alerted and send no second email.

## Required outcomes / tasks

- [ ] Screenshot of the mail sink (Mailpit web UI or aiosmtpd terminal) showing one consolidated alert email, system clock visible.
- [ ] Both alert_workflow.py and alert_workflow.js submitted.
- [ ] Extend either script with your own list of 5 resources and a budget equal to the last two digits of your roll number; show the consolidated email.
- [ ] Output of `SELECT * FROM alerts;` after the state extension, and a second run that sends no email.

## Code files in this lab

- [`code/alert_workflow.js`](code/alert_workflow.js)
- [`code/alert_workflow.py`](code/alert_workflow.py)
- [`code/alert_workflow_stateful.py`](code/alert_workflow_stateful.py)
