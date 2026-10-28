import requests, csv, datetime
from bs4 import BeautifulSoup
r = requests.get(url, headers={"User-Agent": "HamdardLab/1.0"}, timeout=10)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")
rows = [{"title": a.get_text(strip=True), "href": a.get("href")} for a in soup.select("a")]
