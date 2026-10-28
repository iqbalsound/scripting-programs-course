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
