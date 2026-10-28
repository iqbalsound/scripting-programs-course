# Week 6: Web Scraping and Threat/Status Data Feeds

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 1 (Apply) | Sweigart, Automate the Boring Stuff, Ch. 12 | Scrape to CSV |


### Learning objectives

- Fetch and parse HTML with `requests` and BeautifulSoup.
- Scrape ethically: robots.txt, terms of use, rate limiting, identification.
- Store results in CSV.


### Hour 1: Web scraping concepts

- HTTP GET, HTML structure, CSS selectors, `soup.select()`.
- Prefer a documented feed or API over scraping a page when one exists.
- **Ethics and law:** check `robots.txt` and the terms; send a clear `User-Agent`; sleep between requests; never scrape personal data.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Targets: public threat-intelligence feeds that permit automated access (check the terms), or a static test page the instructor hosts.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Targets: cloud-provider status pages and RSS/JSON status feeds, or an instructor-hosted test page.


### Hour 2: Data storage

- Write rows with `csv.DictWriter`; include a `collected_at` UTC column and the source URL.
- Cloud track: write the CSV to a bucket on the emulator, or insert into SQLite as a stand-in for a cloud database.


### Hour 3: Lab

- Scrape a page or feed, extract at least three fields, store them in CSV with timestamps.
- Handle a missing element without crashing.

```python
import requests, csv, datetime
from bs4 import BeautifulSoup
r = requests.get(url, headers={"User-Agent": "HamdardLab/1.0"}, timeout=10)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")
rows = [{"title": a.get_text(strip=True), "href": a.get("href")} for a in soup.select("a")]
```

> 📁 Saved as [`code/example_01.py`](code/example_01.py)


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalized, see the Appendix on personalization.

1. State the exact URL scraped, paste the first five rows of your CSV, and show the `robots.txt` line you checked.
1. Show the `collected_at` value of your first row and your system clock at that moment.
1. Make one selector fail on purpose and paste how your script behaved.
1. Show the line of code that rate-limits your requests and explain the interval you chose.
1. Why is an official API or feed preferred over scraping HTML for the same data? Answer using a specific difference you saw in your own output.

## Code files in this week

- [`code/example_01.py`](code/example_01.py)
