import csv, random, datetime

random.seed(42)                      # same data on every run, so answers can be checked
now = datetime.datetime.now(datetime.timezone.utc)
rows = []
for i in range(50):
    ts = now - datetime.timedelta(minutes=i * 7)
    rows.append([ts.isoformat(timespec="seconds"), f"host-{random.randint(1, 5)}",
                 random.choice(["INFO", "WARN", "ERROR"]), f"event id {i}"])
with open("sample_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "host", "level", "message"])
    writer.writerows(rows)
print("sample_data.csv generated")
