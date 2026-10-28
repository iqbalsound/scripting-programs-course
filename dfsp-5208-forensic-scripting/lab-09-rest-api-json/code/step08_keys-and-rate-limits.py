import os, time
API_KEY = os.getenv("API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
resp = requests.get(URL, headers=headers, timeout=10)
if resp.status_code == 429:
    time.sleep(int(resp.headers.get("Retry-After", "5")))
    resp = requests.get(URL, headers=headers, timeout=10)
