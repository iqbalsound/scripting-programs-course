import csv, random

random.seed(42)
regions = ["us-east-1", "eu-west-1", "ap-south-1"]
statuses = ["running", "stopped", "degraded"]
with open("resources.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "region", "status"])
    for i in range(1, 31):
        writer.writerow([f"res-{i:03d}", random.choice(regions), random.choice(statuses)])
print("resources.csv generated")
