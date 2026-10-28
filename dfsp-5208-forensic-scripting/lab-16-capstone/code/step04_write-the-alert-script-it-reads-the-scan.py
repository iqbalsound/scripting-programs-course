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
