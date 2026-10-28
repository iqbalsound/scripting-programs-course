import os, json, hashlib, datetime, logging
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = os.getenv("API_URL", "https://api.abuseipdb.com/api/v2/check")

def utc_stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")

def fetch_ip(ip):
    headers = {"Key": API_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}
    resp = requests.get(URL, headers=headers, params=params, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
    return resp.json()

def save_evidence(data, url):
    ts = utc_stamp()
    fname = f"evidence_{ts}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    with open(fname, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    with open("custody.log", "a", encoding="utf-8") as log:
        log.write(f"{ts}\t{url}\t{fname}\tSHA256={digest}\n")
    return fname, digest

if __name__ == "__main__":
    try:
        data = fetch_ip("203.0.113.9")
        print(save_evidence(data, URL))
        print("score:", data.get("data", {}).get("abuseConfidenceScore"))
    except requests.exceptions.RequestException as e:
        print("Network failure:", e)
    except RuntimeError as e:
        print("API failure:", e)
