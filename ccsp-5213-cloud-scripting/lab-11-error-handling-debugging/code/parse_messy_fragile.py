import csv

def parse_row(row):
    return {"resource": row["resource"], "cost": float(row["cost"])}
# crashes on non-numeric cost

with open("messy_billing.csv") as f:
    for row in csv.DictReader(f):
        print(parse_row(row))
