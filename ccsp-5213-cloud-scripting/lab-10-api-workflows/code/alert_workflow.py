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
