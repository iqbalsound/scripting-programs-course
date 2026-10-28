import csv, sys, time
import requests
from bs4 import BeautifulSoup

URL = sys.argv[1] if len(sys.argv) > 1 else "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Lab06-Student-Scraper/1.0 (course exercise)"}

try:
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
except requests.exceptions.Timeout:
    sys.exit(f"Timed out fetching {URL}")
except requests.exceptions.RequestException as exc:
    sys.exit(f"Request failed: {exc}")

soup = BeautifulSoup(resp.text, "html.parser")
rows = []
for book in soup.select("article.product_pod"):
    link = book.h3.a if book.h3 else None
    price = book.select_one(".price_color")
    if link is None or price is None:                     # tolerate a missing element
        print("skipped one malformed item", file=sys.stderr)
        continue
    rows.append([link["title"], price.text.strip()])

with open("scraped_books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "price"])
    writer.writerows(rows)
print(f"Saved {len(rows)} records to scraped_books.csv")
time.sleep(1)                                              # one request, then a polite pause before any next page
