# Lab 6: Web Scraping with Python (BeautifulSoup)

**Course:** CCSP-5213  |  **Lecture week:** 6  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Install and use BeautifulSoup4 and requests — both free, open-source Python libraries.
- Extract structured data from a public web page and store it as CSV.
- Respect robots.txt and apply polite scraping practices (rate limiting, User-Agent headers).

## Short theory

Web scraping automates the collection of publicly available web data in cloud work this ranges from gathering open-source threat intelligence to monitoring cloud-service status pages. `requests` fetches the raw HTML and `BeautifulSoup4` (both free/open source, installed via pip) parses it into a navigable tree so specific elements (tables, links, headlines) can be extracted programmatically instead of read by eye.
When a cloud provider's status page offers an RSS or JSON feed, prefer the feed over scraping its HTML: it is more stable and puts less load on the server.

## Prerequisites

- Labs 1–3 completed (Python + venv working).
- Internet access to reach a public test page (or use the local test page in Step 5 if the site is unreachable).

## Step-by-step solution


### Step 1: Install the libraries (free, from PyPI)


```bash
cd ~/cloud-scripting && mkdir lab06 && cd lab06
source ../lab01/.venv/bin/activate
pip install requests beautifulsoup4
```


### Step 2: Check the target site's scraping policy

Before scraping any site, open its /robots.txt and confirm the path you intend to fetch is not disallowed. For this lab we use https://books.toscrape.com, a site built specifically for scraping practice.

### Step 3: Write the scraper

The scraper identifies itself with a User-Agent, sets a timeout, handles network errors with try/except, tolerates a malformed item instead of crashing, and pauses between requests (a pause placed inside a loop over results that are already downloaded would not rate-limit anything).

```python
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
```

> 📁 Saved as [`code/step03_write-the-scraper.py`](code/step03_write-the-scraper.py)


### Step 4: Run and inspect the output


```bash
python scraper.py
head -5 scraped_books.csv
```

On the real site the first page returns 20 books.

### Step 5: Test offline against a local page and a failure

Public sites are not always reachable. Create a tiny local page that contains one good item and one malformed item, serve it, and run the scraper against it. Then point the scraper at a port where nothing is listening to see the error handling.

```bash
mkdir -p testpage && cat > testpage/index.html <<'EOF'
<html><body>
<article class="product_pod"><h3><a title="Local Book One"
href="#">Local Book One</a></h3><p
class="price_color">&pound;10.00</p></article>
<article class="product_pod"><h3><a title="Broken Item"
href="#">Broken Item</a></h3></article>
</body></html>
EOF
python3 -m http.server 8765 --directory testpage &
python scraper.py http://127.0.0.1:8765/     # skipped one malformed item, Saved 1 records
python scraper.py http://127.0.0.1:1/ ; echo "exit code: $?"   # Request failed ..., exit code 1
kill %1
```

The same code works for a status or threat-intelligence page: change the URL and the CSS selectors, and prefer a feed when one exists.

## Required outcomes / tasks

- [ ] scraper.py and scraped_books.csv submitted, with a screenshot of the run (system clock visible).
- [ ] Screenshot of the offline test (one record saved, one malformed item skipped) and of the failure case with its exit code.
- [ ] Extend the scraper to follow the “next” page link for up to 3 pages, with a 1-second pause between page requests.
- [ ] One paragraph explaining what robots.txt is and why rate limiting matters ethically and legally.

## Code files in this lab

- [`code/step03_write-the-scraper.py`](code/step03_write-the-scraper.py)
