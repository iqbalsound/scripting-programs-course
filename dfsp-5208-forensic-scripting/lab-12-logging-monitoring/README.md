# Lab 12: Logging and Monitoring in Security Scripts

**Course:** DFSP-5208  |  **Lecture week:** 13  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Replace ad-hoc print statements with Python's `logging` module and Node's `winston` (both free/OSS).
- Configure log levels, rotation, console output and structured (JSON) output.
- Make a log tamper-evident with a SHA-256 hash, and view and filter logs quickly using `lnav` (free, open-source log file navigator).

## Short theory

Print statements do not scale: they cannot be filtered by severity, timestamped consistently, or redirected without editing code. Python's `logging` module (standard library, free) and Node's `winston` package (MIT-licensed, free) provide leveled, structured logging with rotation support, matching what is expected of production-grade forensic tooling. `lnav` is a free terminal-based log viewer that auto-detects formats and supports live filtering.

## Prerequisites

- Lab 11 completed.
- lnav installed (sudo `apt install` lnav).

## Step-by-step solution


### Step 1: Configure Python logging with rotation, JSON output and a console handler

One logger writes a text log, a JSON-lines log (one JSON object per line, easy for tools to read) and prints warnings and errors to the console. Both files rotate at 1 MB, keeping 3 old files.

```bash
cd ~/forensic-scripting && mkdir lab12 && cd lab12 &&
source ../lab01/.venv/bin/activate
```


```python
import datetime, json, logging, sys
from logging.handlers import RotatingFileHandler


class JsonFormatter(logging.Formatter):
    def format(self, r):
        return json.dumps({"ts": datetime.datetime.fromtimestamp(r.created, datetime.timezone.utc).isoformat(),
                           "level": r.levelname, "msg": r.getMessage(), "logger": r.name,
                           "context": getattr(r, "context", {})})


def make_logger(name="pipeline", max_bytes=1_000_000):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    text = RotatingFileHandler("pipeline.log", maxBytes=max_bytes, backupCount=3, encoding="utf-8")
    text.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    jsonl = RotatingFileHandler("pipeline.jsonl", maxBytes=max_bytes, backupCount=3, encoding="utf-8")
    jsonl.setFormatter(JsonFormatter())
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.WARNING)
    for h in (text, jsonl, console):
        logger.addHandler(h)
    return logger


if __name__ == "__main__":
    log = make_logger()
    log.info("Pipeline started", extra={"context": {"case": "C-001"}})
    log.warning("Suspicious file skipped: corrupt_evidence.dat")
    log.error("Failed to hash file: permission denied")
```

> 📁 Saved as [`code/step01_configure-python-logging-with-rotation-j.py`](code/step01_configure-python-logging-with-rotation-j.py)


### Step 2: Run it and read the three outputs


```bash
python logger_demo.py
cat pipeline.log
cat pipeline.jsonl
```

Expected: the text log has three lines with a time stamp and level, the JSON log has the same events as JSON objects, and only the WARNING and ERROR messages appear on the console.

### Step 3: Install and configure winston (Node.js)


```bash
npm install winston
```


### Step 4: Write logger.js with built-in rotation

Winston's File transport already rotates with maxsize and maxFiles, so no extra package is needed (winston-daily-rotate-file is also acceptable if you prefer daily files).

```javascript
const winston = require('winston');
const logger = winston.createLogger({
  level: 'debug',
  format: winston.format.combine(winston.format.timestamp(), winston.format.json()),
  transports: [
    new winston.transports.File({ filename: 'pipeline.json.log', maxsize: 1_000_000, maxFiles: 3 }),
    new winston.transports.Console(),
  ],
});
logger.info('Pipeline started');
logger.warn('Suspicious file skipped: corrupt_evidence.dat'); logger.error('Failed to hash file: permission denied');
```

> 📁 Saved as [`code/logger.js`](code/logger.js)


### Step 5: Make a closed log tamper-evident

Lower max_bytes in the Python script to about 2000 and write 100 extra log lines in a loop so that the log rotates and a closed file such as pipeline.log.1 appears. Hash that closed file, store the hash somewhere else, and verify it later. The live pipeline.log changes with every line, so it must never be hashed while it is open.

```bash
# set maxBytes small (e.g. 2000) so the log rotates, then hash a CLOSED file:
sha256sum pipeline.log.1 >> log_hashes.txt
# later, verify:
sha256sum -c log_hashes.txt        # OK, or FAILED if one character was changed
```

Change one character in pipeline.log.1 and run the verification again: it must report FAILED.

### Step 6: Inspect logs with lnav


```bash
lnav pipeline.log
# inside lnav: press e / E to jump to the next / previous error line,
# or type  :filter-in WARNING|ERROR  to show only those lines
```

Key bindings vary slightly between lnav versions; take the screenshot of the filtered view.

## Required outcomes / tasks

- [ ] pipeline.log, pipeline.jsonl and pipeline.json.log submitted, with at least one message at each of the INFO, WARNING and ERROR levels.
- [ ] Screenshot of lnav showing a filtered view (only WARNING/ERROR lines), with the system clock visible.
- [ ] A rotated file (pipeline.log.1), its hash recorded in log_hashes.txt, and a screenshot of `sha256sum -c log_hashes.txt` showing OK, then FAILED after you change one character.
- [ ] Configure winston so that no single file exceeds 1 MB (maxsize and maxFiles, or winston-daily-rotate-file) and show the setting.

## Code files in this lab

- [`code/logger.js`](code/logger.js)
- [`code/step01_configure-python-logging-with-rotation-j.py`](code/step01_configure-python-logging-with-rotation-j.py)
