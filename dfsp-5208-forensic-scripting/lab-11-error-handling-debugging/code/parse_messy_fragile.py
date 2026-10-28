import csv

def parse_row(row):
    return {
        "timestamp": row["timestamp"],
        "severity": int(row["severity"]),   # will crash on non-numeric values
    }

with open("messy_log.csv") as f:
    for row in csv.DictReader(f):
        print(parse_row(row))
