import requests
with_retry(lambda: requests.get("http://127.0.0.1:1", timeout=5).raise_for_status(),
           attempts=2, delay=0.1, retry_on=(requests.exceptions.RequestException,))
