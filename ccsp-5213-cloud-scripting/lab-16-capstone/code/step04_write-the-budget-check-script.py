"""Send each filtered usage row to the usage-alert function and collect the answers."""
import csv, json, os, subprocess, sys, urllib.request

src, dst = sys.argv[1], sys.argv[2]
url = os.getenv("SCAN_URL")                      # e.g. http://host.docker.internal:8080/function/usage-alert
results = []
with open(src, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        payload = json.dumps({"resource": row["resource"], "costUsd": row["costUsd"]})
        if url:
            req = urllib.request.Request(url, data=payload.encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                results.append(json.load(r))
        else:
            out = subprocess.run(["node", "faas/harness.js", "faas/handler.js", payload], capture_output=True, text=True, check=True)
            results.append(json.loads(out.stdout)["body"])
with open(dst, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
errors = [r for r in results if "error" in r]
over = [r for r in results if r.get("overBudget")]
print(f"{len(results) - len(errors)} resources checked, {len(errors)} rejected as invalid, {len(over)} over budget: {[r['resource'] for r in over]}")
