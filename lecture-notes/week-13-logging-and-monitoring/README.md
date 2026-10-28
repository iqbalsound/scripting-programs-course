# Week 13: Logging and Monitoring

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 3 (Analyze) | Python "Logging HOWTO" and "Logging Cookbook" (docs.python.org); Winston README; Grafana Loki documentation | Python logging, Winston, optional Loki |

> Revised for Fall 2026 Reading changed: *Docker Deep Dive* Ch. 2-3 does not cover logging; move it to Week 14 where it fits. Promtail is deprecated in favour of Grafana Alloy (support ended in early 2026). The Cloud track step that "points Promtail at the log file" should use Grafana Alloy, or the simpler fallback below (push lines to Loki's HTTP API). Check Grafana's current docs for the configuration syntax. The original basicConfig(filename=...) and RotatingFileHandler snippets conflicted. A single correct configuration is given below. The "hash at start and end" exercise is revised: a log that is still being written changes by definition. Hash closed (rotated) files and store the hashes elsewhere.


### Learning objectives

- Explain why persistent, timestamped, severity-tagged logs differ from `print` debugging.
- Configure Python logging with console, rotating file and JSON handlers.
- Implement equivalent logging in Node.js with Winston.
- Describe how logs are aggregated and how tampering can be detected.


### Hour 1: Why logging matters

- A log is persistent process evidence: it outlives the run and is read by someone else (an auditor, an on-call engineer).
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. INFO for normal operation, ERROR for real failures; misusing levels makes logs useless.
- Timestamps in UTC with timezone, consistent format, no secrets in logs.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Admissibility theme: you must be able to show what the tool did and when, and that the record was not altered afterwards.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Operations theme: an on-call engineer diagnoses an incident hours later using only the log.


### Hour 2: Structured logging in Python

- Replace every `print()` with the right level.
- `RotatingFileHandler` caps size and keeps backups, so a long-running monitor does not fill the disk.
- Emit JSON lines so logs can be queried without fragile text parsing.

```python
import logging, json, datetime
from logging.handlers import RotatingFileHandler

class JsonFormatter(logging.Formatter):
    def format(self, r):
        return json.dumps({
            "ts": datetime.datetime.fromtimestamp(r.created, datetime.timezone.utc).isoformat(),
            "level": r.levelname, "msg": r.getMessage(),
            "logger": r.name, "context": getattr(r, "context", {}),
        })

log = logging.getLogger("workflow")
log.setLevel(logging.INFO)
text = RotatingFileHandler("workflow.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8")
text.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
jsonl = RotatingFileHandler("workflow.jsonl", maxBytes=5_000_000, backupCount=3, encoding="utf-8")
jsonl.setFormatter(JsonFormatter())
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
for hd in (text, jsonl, console):
    log.addHandler(hd)

log.info("fetched", extra={"context": {"entity": "203.0.113.9", "score": 77}})
```

> 📁 Saved as [`code/example_01.py`](code/example_01.py)


### Hour 3: Winston and an open-source monitoring stack

- Winston: levels, transports (console and file together), formats.
- Grafana Loki + Grafana are free, self-hosted log aggregation and search.
- Tamper evidence: store the hash of each **closed** log file in a separate append-only record or a different system. Optional extension: a hash chain where each line carries the hash of the previous line.

```javascript
const winston = require("winston");
const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(winston.format.timestamp(), winston.format.json()),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "workflow.log" }),
  ],
});
logger.error("fetch failed", { url, err: err.message });
```

> 📁 Saved as [`code/example_02.js`](code/example_02.js)

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Fallback if Alloy is unavailable: start Loki with docker run -d -p 3100:3100 grafana/loki and Grafana with docker run -d -p 3000:3000 grafana/grafana, then push a line from Python with a POST to http://localhost:3100/loki/api/v1/push using a JSON body {"streams":[{"stream":{"job":"lab"},"values":[["<unix-ns-timestamp>","<line>"]]}]}. Add Loki as a data source in Grafana (URL http://host.docker.internal:3100, or a shared Docker network) and query {job="lab"} in Explore.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Loki/Grafana is optional for this track. The required tamper-evidence exercise is the hash of a rotated log file recorded in a separate file, then re-verified.


### Step-by-step lab method (free and open-source tools only)

**Tools:** Python `logging`, Winston (`npm install winston`), `sha256sum` or `Get-FileHash`; optional Docker with Loki and Grafana.

1. Add the logging configuration above to your Week 12 script.
1. Replace all remaining `print()` calls with the correct level.
1. Set `maxBytes=2000` temporarily and run until the file rotates; then restore 5 MB.
1. Add Winston to a Node.js script with console and file transports.
1. Trigger one deliberate error in each script and confirm it appears at ERROR level in both logs.
1. Hash a rotated (closed) log file, store the hash in `hashes.txt`, change one character in a copy, and re-verify.
1. Add a retention-policy comment at the top of each script (how long logs are kept and why).
1. **Cloud:** run Loki and Grafana and view your logs in Explore. **Forensic:** optional.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalised, see the Appendix on personalisation.

1. Paste the exact log lines your script produced for one INFO and one ERROR event, including the timestamp.
1. Trigger rotation (set `maxBytes` to 2000) and list the files that appeared. If you cannot, calculate how many average-length lines fit in 5,000,000 bytes using a line length you measured.
1. Paste the console and file output Winston produced for one deliberate error.
1. Hash a rotated log file and paste the SHA-256. Then change one character in a copy and paste its hash. Explain what a verifier would conclude.
1. Show one real JSON log entry and the exact Python code that produced it.
1. **Cloud:** screenshot of your log stream in Grafana Explore with the query used. **Forensic:** the exact `docker run` command you would use to start Loki, and the port it exposes.
1. Identify one log statement using the wrong severity and give the corrected line.
1. Explain, using your retention-policy comment, how a longer or shorter retention period would change the usefulness of this log (evidential for Forensic, diagnostic for Cloud).

## Code files in this week

- [`code/example_01.py`](code/example_01.py)
- [`code/example_02.js`](code/example_02.js)
