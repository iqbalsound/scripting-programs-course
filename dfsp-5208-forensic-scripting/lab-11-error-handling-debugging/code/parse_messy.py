import csv, logging, time

logging.basicConfig(filename="parse_errors.log", level=logging.WARNING,
                    format="%(asctime)s %(levelname)s %(message)s")


class RetryExhausted(Exception):
    """Raised when every attempt of a retried operation has failed."""


def parse_row(row):
    try:
        return {"timestamp": row["timestamp"], "severity": int(row["severity"])}
    except (KeyError, ValueError, TypeError) as exc:
        logging.warning("Skipped malformed row %r: %s", row, exc)
        return None


def with_retry(fn, attempts=3, delay=1.0, retry_on=(OSError,)):
    """Retry fn on transient errors. requests' exceptions subclass OSError, NOT the builtin ConnectionError."""
    for i in range(1, attempts + 1):
        try:
            return fn()
        except retry_on as exc:
            logging.warning("Attempt %d/%d failed: %s", i, attempts, exc)
            time.sleep(delay * 2 ** (i - 1))
    raise RetryExhausted(f"all {attempts} attempts failed")


if __name__ == "__main__":
    results = []
    try:
        with open("messy_log.csv", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                parsed = parse_row(row)
                if parsed:
                    results.append(parsed)
    except FileNotFoundError:
        logging.error("messy_log.csv not found")
        raise SystemExit("messy_log.csv not found")
    print(f"Successfully parsed {len(results)} rows; see parse_errors.log for skipped rows")
