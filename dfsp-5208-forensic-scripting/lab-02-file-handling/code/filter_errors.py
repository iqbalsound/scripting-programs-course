import csv, datetime
from pathlib import Path

src, dst = Path("sample_data.csv"), Path("errors_only.csv")
counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
with src.open(newline="", encoding="utf-8") as inp, dst.open("w", newline="", encoding="utf-8") as out:
    reader = csv.DictReader(inp)
    writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        counts[row["level"]] = counts.get(row["level"], 0) + 1
        if row["level"] == "ERROR":
            writer.writerow(row)
print(f"{counts['ERROR']} ERROR rows written to {dst}; {counts['WARN']} WARN rows seen; {counts['INFO']} INFO rows seen")

with open("run_history.log", "a", encoding="utf-8") as log:
    log.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')} - filter_errors.py executed\n")
