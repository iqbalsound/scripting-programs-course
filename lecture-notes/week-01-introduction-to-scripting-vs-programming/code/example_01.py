import platform, datetime, hashlib, pathlib
me = pathlib.Path(__file__).read_bytes()
print("Host :", platform.node())
print("UTC  :", datetime.datetime.now(datetime.timezone.utc).isoformat())
print("SHA256 of this script:", hashlib.sha256(me).hexdigest())
