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
