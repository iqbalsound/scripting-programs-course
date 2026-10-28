# Week 10: API Interaction: REST APIs and JSON Parsing

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 1 (Apply) | ATBS (2nd ed.) Ch. 16 (CSV and JSON); Python requests Quickstart; HTTP status codes (MDN) | Fetch, parse, save and hash evidence |

> Revised for Fall 2026 Reading changed: *Practical Malware Analysis* Ch. 6 is about x86 control flow, not APIs. Cloud track: LocalStack Community is no longer freely available; use Moto server (or Floci / LocalStack with a free token). datetime.utcnow() is deprecated; the scripts below use timezone-aware UTC. Node.js parity added because Assignment 2 is a Node.js API task. Fallback mock API added so the lab works even if a free-tier API is down or rate-limited.


### Learning objectives

- Explain REST principles (resources, verbs, statelessness) and HTTP status code classes.
- Parse nested JSON safely with `dict.get`, `try/except KeyError` and type checks.
- Build authenticated, time-limited, error-tolerant requests with Python `requests` and Node.js `fetch`.
- Persist responses as timestamped files with a SHA-256 hash and an audit log entry.


### Hour 1: REST, HTTP and status codes

- An API is a contract between programs. REST uses URLs for resources and verbs: GET reads, POST creates, PUT/PATCH updates, DELETE removes.
- Status classes: 2xx success; 4xx client problem (401 unauthenticated, 403 forbidden, 404 not found, 429 rate limit); 5xx server failure. A script that treats a 403 as data corrupts the record.
- Credentials travel in headers (API key, bearer token). They must never be hard-coded or committed. Store them in `.env` and add `.env` to `.gitignore` on day one.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Platforms such as VirusTotal, AbuseIPDB and Shodan expose reputation data over REST. Scripting the call gives a reproducible, timestamped record, which supports chain of custody.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) AWS, Azure and GCP expose every service over REST beneath the SDKs. A 403 usually means an IAM permission problem; a script that carries on would act on a false assumption.


### Hour 2: JSON as the data-interchange format

- JSON objects map to Python dicts and arrays to lists; `response.json()` or `json.loads()` converts text to Python objects.
- Real responses are nested and vary between vendors and versions: use `data.get("data", {}).get("abuseConfidenceScore")` or catch `KeyError`.
- Check types before comparing (is the score really an `int`?). Schemas change silently.
- Why JSON and not a flat CSV row? Nested objects and arrays (list of detections, list of resources) do not fit one row without losing structure.


### Hour 3: Python workflow with requests

- Always pass `timeout=`; check `status_code` before parsing; catch `requests.exceptions.RequestException`.
- Save the raw JSON immediately with a UTC timestamp in the file name ("evidence at rest"), compute its SHA-256, and append a line to a custody/audit log.
- Node.js parity: Node 18+ has built-in `fetch`; the same discipline applies.

```python
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
```

> 📁 Saved as [`code/example_01.py`](code/example_01.py)

**Node.js equivalent (for Assignment 2):**

```javascript
const fs = require("fs/promises");
require("dotenv").config();

async function main() {
  try {
    const res = await fetch(process.env.API_URL, {
      headers: { Key: process.env.API_KEY, Accept: "application/json" },
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const ts = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15);
    await fs.writeFile(`evidence_${ts}.json`, JSON.stringify(data, null, 2));
    console.log("saved", ts);
  } catch (err) {
    console.error("Fetch failed:", err.message);
    process.exitCode = 1;
  }
}
main();
```

> 📁 Saved as [`code/example_02.js`](code/example_02.js)

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Query a free-tier threat-intelligence API for one IP address (use documentation or test addresses such as 203.0.113.0/24 where the provider allows). Free-tier daily limits and header names change; check the provider's current documentation before the lab.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Start a local emulator and query it as you would a real endpoint. With Moto: pip install "moto[server]" then moto_server -p 5000. Create a bucket with boto3 (dummy credentials test/test, endpoint_url="http://localhost:5000"), then call requests.get(BASE + STATE_PATH) where STATE_PATH is /moto-api/data.json (confirm on your installed version). If you use LocalStack with a free token, the health path is /_localstack/health. Keep CLOUD_URL and STATE_PATH in .env so the same script runs on any emulator.


#### Instructor fallback: 25-line mock API

Run this on the instructor PC or on each student machine (`python mock_api.py`). It returns 401 for a wrong key, 200 for the first three valid calls and 429 afterwards. Restart it to reset the counter. Point `API_URL` at `http://127.0.0.1:8000/` and use the key `lab-key`.

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, datetime
calls = 0
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        global calls
        if self.headers.get("Key") != "lab-key":
            return self._send(401, {"errors": [{"detail": "Authentication failed"}]})
        calls += 1
        if calls > 3:
            return self._send(429, {"errors": [{"detail": "Rate limit exceeded"}]})
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self._send(200, {"data": {"ipAddress": "203.0.113.9", "abuseConfidenceScore": 77,
                                  "totalReports": 12, "lastReportedAt": now}})
    def _send(self, code, body):
        b = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
HTTPServer(("127.0.0.1", 8000), H).serve_forever()
```

> 📁 Saved as [`code/mock_api.py`](code/mock_api.py)


### Step-by-step lab method (free and open-source tools only)

**Tools:** Python 3.12+, VS Code, `requests`, `python-dotenv`; Node.js LTS; Forensic: any free-tier threat-intelligence API or the mock; Cloud: Moto server (or Floci / LocalStack with free token).

1. Create a project folder and a virtual environment (see command table in Section 3), then `pip install requests python-dotenv`.
1. Create `.env` with `API_KEY=...` and `API_URL=...` and add `.env` to `.gitignore` **before** the first commit.
1. Write `api_lookup.py` as above. Run it and confirm a 200 response.
1. Open the saved JSON and identify the nested structure: list the top-level keys and one nested field.
1. Record the SHA-256 of the saved file and compare it with the hash in `custody.log`.
1. Re-run with an invalid key (or stopped emulator) and record the status code or connection error.
1. Run three rapid requests (mock API: observe the 429 on the fourth call).
1. Write the Node.js version and save a second timestamped file.
1. Commit the code (not the evidence, not `.env`) and push.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalised, see the Appendix on personalisation.

1. Execute a live GET request from your machine and report the exact HTTP status code and the first five top-level keys of the returned JSON. Include a screenshot showing the system clock.
1. **Forensic:** send an invalid API key and paste the exact status code and JSON error message. **Cloud:** stop the emulator and paste the exact connection error.
1. From the response you retrieved, extract one nested field of your choosing. Show the single line of Python used and the value.
1. Using the file you saved, explain why a nested JSON object rather than a flat CSV row was necessary. Refer to the real structure you observed.
1. Compute the SHA-256 of the saved JSON file and paste the exact terminal output of the command.
1. Send four rapid requests to the mock API (or three to the real one). Report the status code of each call and explain what safeguard (or limit) produced it.
1. Show your `.env` structure with the key redacted, the Python lines that load it, and one sentence on why hard-coding a credential is a security risk. Show `git status` proving `.env` is ignored.
1. Compare the timestamp inside the JSON payload (if present) with your system clock at the time of the request. Explain any difference you observed (time zone, clock skew, caching).

## Code files in this week

- [`code/example_01.py`](code/example_01.py)
- [`code/example_02.js`](code/example_02.js)
- [`code/mock_api.py`](code/mock_api.py)
