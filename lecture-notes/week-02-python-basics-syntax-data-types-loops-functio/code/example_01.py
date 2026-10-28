def parse_line(line):
    parts = line.strip().split()
    if len(parts) < 4:
        return None
    return {"date": parts[0], "time": parts[1], "event": parts[2]}

counts, skipped = {}, 0
with open("sample.log", encoding="utf-8") as f:
    for line in f:
        rec = parse_line(line)
        if rec is None:
            skipped += 1
            continue
        counts[rec["event"]] = counts.get(rec["event"], 0) + 1
print(counts, "skipped:", skipped)
