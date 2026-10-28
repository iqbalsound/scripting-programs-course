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
    log.info("Deployment pipeline started", extra={"context": {"resource": "vm-01", "region": "us-east-1"}})
    log.warning("Resource vm-01 approaching budget limit")
    log.error("Failed to provision resource: quota exceeded")
