# Lab 9: REST API Interaction: Fetching and Parsing JSON Data

**Course:** DFSP-5208  |  **Lecture week:** 10  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Send GET requests to a REST API using Python `requests` and Node.js fetch/axios (free, OSS) and handle non-200 responses explicitly.
- Parse JSON responses and extract fields relevant to a forensic case timeline.
- Preserve each response as timestamped evidence with a SHA-256 hash and a custody-log entry, then store parsed records in a local SQLite database file.

## Short theory

Forensic tooling frequently needs to pull data from external services, threat-intel feeds, case-management systems, breach-notification APIs. REST APIs exchange data as JSON over HTTP(S). Python's `requests` and Node's `axios` (installed free via pip/npm) are the de-facto open-source libraries for this. SQLite, built into Python's standard library and free everywhere, is used here in place of a paid cloud database so the lab requires no account or billing setup.
Evidence handling matters even for API data: save the raw response in a file whose name carries a UTC timestamp, record its SHA-256 hash, and append a line to a custody log. Anyone can then check later that the file has not changed. Never parse an error response as if it were data: check the status code first.

## Prerequisites

- Labs 1–3 and 7 completed.
- Internet access to a public test API (https://jsonplaceholder.typicode.com), or the local mock API in Step 2 if it is unreachable.

## Step-by-step solution


### Step 1: Set up the project


```bash
cd ~/forensic-scripting && mkdir lab09 && cd lab09
source ../lab01/.venv/bin/activate
pip install requests
sudo apt install -y sqlite3     # command-line client used in Step 5
```


### Step 2: Start the local mock API (optional fallback)

If the public API is unreachable, create mock_api.py and run it in a second terminal. Then point the scripts at it with the API_URL environment variable; leave API_URL unset to use the public site.

```python
# mock_api.py - a tiny local stand-in for the public test API (no internet needed)
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

POSTS = [{"userId": (i % 5) + 1, "id": i, "title": f"case note {i}", "body": f"details for note {i}"}
         for i in range(1, 101)]
TODOS = [{"userId": (i % 5) + 1, "id": i, "title": f"resource task {i}", "completed": i % 3 == 0}
         for i in range(1, 101)]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {"/posts": POSTS, "/todos": TODOS}.get(self.path)
        code = 200 if data is not None else 404
        body = json.dumps(data if data is not None else {"error": "not found"}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):      # keep the terminal quiet
        pass

if __name__ == "__main__":
    print("Mock API listening on http://127.0.0.1:8765 (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
```

> 📁 Saved as [`code/mock_api.py`](code/mock_api.py)


```bash
python mock_api.py &
export API_URL=http://127.0.0.1:8765
```


### Step 3: Write fetch_cases.py (evidence workflow)

The script checks the status code before parsing, saves the raw response as a timestamped evidence file, hashes it, writes a custody-log line, and stores 20 parsed records with a parameterized SQL statement.

```python
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
```

> 📁 Saved as [`code/fetch_cases.py`](code/fetch_cases.py)


### Step 4: Run it and verify the evidence


```bash
python fetch_cases.py
cat custody.log
sha256sum evidence_*.json     # must match the SHA256 value in custody.log
```


### Step 5: Query the stored data


```bash
sqlite3 case_notes.db "SELECT id, title FROM notes LIMIT 5;"
```


### Step 6: Node.js equivalent with the built-in fetch

Node.js includes fetch, so no extra package is needed. Write fetch_cases.js:

```javascript
const BASE = process.env.API_URL || 'https://jsonplaceholder.typicode.com';

async function main() {
  try {
    const res = await fetch(`${BASE}/posts`, { signal: AbortSignal.timeout(10000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);          // non-200 handled explicitly
    const data = await res.json();
    console.table(data.slice(0, 5).map(p => ({ id: p.id, title: p.title })));
  } catch (err) {
    console.error('API error:', err.message);
    process.exitCode = 1;
  }
}
main();
```

> 📁 Saved as [`code/fetch_cases.js`](code/fetch_cases.js)

If you prefer axios (free, OSS), install it with npm install axios and use this version, which also handles a non-200 status explicitly:

```javascript
const url = (process.env.API_URL || 'https://jsonplaceholder.typicode.com') + '/posts';
const axios = require('axios');
axios.get(url, { timeout: 10000, validateStatus: () => true })
  .then(res => {
    if (res.status !== 200) throw new Error(`HTTP ${res.status}`);
    console.table(res.data.slice(0, 5).map(p => ({ id: p.id, title: p.title })));
  })
  .catch(err => { console.error('API error:', err.message); process.exitCode = 1; });
```

> 📁 Saved as [`code/step06_fetch_cases.js`](code/step06_fetch_cases.js)


### Step 7: Test the failure paths


```bash
API_URL=http://127.0.0.1:8765/bad python fetch_cases.py; echo "exit code: $?"   # HTTP 404 reported, exit code 1
API_URL=http://127.0.0.1:1 node fetch_cases.js; echo "exit code: $?"
# fetch failed, exit code 1
```


### Step 8: Keys and rate limits

Real APIs need a key and limit how fast you may call them. Never write a key into the code: keep it in a .env file that .gitignore excludes, load it into the environment, and send it in a header. If the server answers 429 (too many requests), wait for the time in the Retry-After header and try again.

```bash
# .env  (never commit this file)
API_KEY=replace-with-your-key

set -a; source .env; set +a      # load it into the environment
```


```python
import os, time
API_KEY = os.getenv("API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
resp = requests.get(URL, headers=headers, timeout=10)
if resp.status_code == 429:
    time.sleep(int(resp.headers.get("Retry-After", "5")))
    resp = requests.get(URL, headers=headers, timeout=10)
```

> 📁 Saved as [`code/step08_keys-and-rate-limits.py`](code/step08_keys-and-rate-limits.py)


## Required outcomes / tasks

- [ ] One evidence_*.json file, custody.log showing its matching SHA-256, and case_notes.db submitted, with a screenshot of the sqlite3 query (system clock visible).
- [ ] fetch_cases.js console.table output screenshot.
- [ ] Screenshots showing both scripts handling a non-200 status or a network failure without crashing, and exiting with a non-zero code.
Add API-key loading from .env and 429 handling (Step 8) to the Python script, and document the behavior in two sentences.

## Code files in this lab

- [`code/fetch_cases.js`](code/fetch_cases.js)
- [`code/fetch_cases.py`](code/fetch_cases.py)
- [`code/mock_api.py`](code/mock_api.py)
- [`code/step06_fetch_cases.js`](code/step06_fetch_cases.js)
- [`code/step08_keys-and-rate-limits.py`](code/step08_keys-and-rate-limits.py)
