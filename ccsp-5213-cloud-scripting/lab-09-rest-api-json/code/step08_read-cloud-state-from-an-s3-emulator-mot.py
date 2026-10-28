import requests
from fetch_resources import save_evidence

URL = "http://localhost:5000/moto-api/data.json"
resp = requests.get(URL, timeout=10)
resp.raise_for_status()
print(save_evidence(resp.json(), URL))
