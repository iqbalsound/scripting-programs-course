import datetime, hashlib, json, os, sqlite3, sys
import requests

BASE = os.getenv("API_URL", "https://jsonplaceholder.typicode.com")
URL = f"{BASE}/posts"


def utc_stamp():
    return
datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")


def fetch(url):
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:                               # non-200: report and stop, never parse an error body
        raise RuntimeError(f"HTTP {resp.status_code} from {url}: {resp.text[:120]}")
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


def store(data):
    conn = sqlite3.connect("case_notes.db")
    with conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, body TEXT)""")
        for item in data[:20]:
            conn.execute("INSERT OR REPLACE INTO notes VALUES (?,?,?,?)",
                         (item["id"], item["userId"], item["title"], item["body"]))
    conn.close()
    return min(len(data), 20)


if __name__ == "__main__":
    try:
        data = fetch(URL)
        print(save_evidence(data, URL))
        print(f"{store(data)} records stored in case_notes.db")
    except requests.exceptions.RequestException as exc:
        sys.exit(f"Network failure: {exc}")
    except RuntimeError as exc:
        sys.exit(f"API failure: {exc}")
