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
