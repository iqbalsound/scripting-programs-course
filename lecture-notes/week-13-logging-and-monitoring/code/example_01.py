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
