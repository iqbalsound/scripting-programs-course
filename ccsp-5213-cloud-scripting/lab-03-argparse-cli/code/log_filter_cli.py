#!/usr/bin/env python3
"""Filter a CSV of log records by level. Usage: log_filter_cli.py --input IN --output OUT [--level L] [--limit N]"""
import argparse, csv, logging, sys
from pathlib import Path

logging.basicConfig(level=logging.INFO,
format="%(asctime)s %(levelname)s %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Filter cloud CSV records by log level.")
    parser.add_argument("--input", required=True, help="Path to source CSV")
    parser.add_argument("--output", required=True, help="Path to write filtered CSV")
    parser.add_argument("--level", default="ERROR", choices=["INFO", "WARN", "ERROR"], help="Level to keep")
    parser.add_argument("--limit", type=int, default=0, help="Stop after N matching rows (0 = no limit)")
    args = parser.parse_args()

    src, dst = Path(args.input), Path(args.output)
    if not src.exists():
        logging.error("Input file not found: %s", src)
        return 1
    dst.parent.mkdir(parents=True, exist_ok=True)

    written = skipped = 0
    with src.open(newline="", encoding="utf-8") as inp, dst.open("w", newline="", encoding="utf-8") as out:
        reader = csv.DictReader(inp)
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
        writer.writeheader()
        for line_no, row in enumerate(reader, start=2):       # line 1 is the header
            level = row.get("level")
            if level is None:
                skipped += 1
                logging.warning("line %d skipped: no 'level' column value", line_no)
                continue
            if level == args.level:
                writer.writerow(row)
                written += 1
                if args.limit and written >= args.limit:
                    break
    print(f"{written} rows with level={args.level} written to {dst} ({skipped} skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
