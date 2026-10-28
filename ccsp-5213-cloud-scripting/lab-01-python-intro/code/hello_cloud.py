import hashlib, pathlib, platform, datetime

ROLL = "YOUR-ROLL-NUMBER"   # replace with your own roll number
print("Scripting environment ready.")
print("Student:", ROLL)
print(f"Python {platform.python_version()} running on {platform.system()}")
print("Course: CCSP-5213 - Scripting Program and Cloud Architecture")
print("UTC:", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
print("SHA256 of this script:", hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
