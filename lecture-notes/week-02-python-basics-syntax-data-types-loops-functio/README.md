# Week 2: Python Basics: Syntax, Data Types, Loops, Functions

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 1 (Apply) | Severance, Python for Everybody, Ch. 2-3 | Parse a log (Forensic) or CSV (Cloud) |

> Revised for Fall 2026 New: a 15-minute exception primer (try/except ValueError) so that students can handle malformed lines in Assignment 1 and the class task before Week 12.


### Learning objectives

- Use variables, core data types, control flow and functions.
- Read a text file line by line and handle a malformed line without crashing.
- Use dictionaries to count occurrences.


### Hour 1: Core syntax

- Dynamic typing; `int`, `float`, `str`, `bool`, `list`, `dict`, `set`, `tuple`.
- Control flow: `if/elif/else`, `for`, `while`, `break`, `continue`.
- Indentation is syntax. Show one indentation bug and read the error message together.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Case study: lines like 2026-03-04 10:22:01 FAILED LOGIN user=admin ip=203.0.113.9. Which fields do you need?

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Case study: a CSV of cloud resources (id,region,status). Which rows are unhealthy?


### Hour 2: Functions, loops and dictionaries

- Write small reusable functions: `parse_line(line)` returns a dict or `None`.
- Counting with a dictionary: `counts[ip] = counts.get(ip, 0) + 1`.
- **Primer:** wrap the parse in `try/except ValueError` and `continue` on bad lines; log how many lines were skipped.

```python
def parse_line(line):
    parts = line.strip().split()
    if len(parts) < 4:
        return None
    return {"date": parts[0], "time": parts[1], "event": parts[2]}

counts, skipped = {}, 0
with open("sample.log", encoding="utf-8") as f:
    for line in f:
        rec = parse_line(line)
        if rec is None:
            skipped += 1
            continue
        counts[rec["event"]] = counts.get(rec["event"], 0) + 1
print(counts, "skipped:", skipped)
```

> 📁 Saved as [`code/example_01.py`](code/example_01.py)


### Hour 3: Hands-on lab

- Instructor supplies `sample.log` (Forensic) or `resources.csv` (Cloud) with a few deliberately broken lines.
- Students count events per type and report the number of skipped lines.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalized, see the Appendix on personalization.

1. Run your parser on the supplied file and paste the exact counts and the skipped-line number.
1. Show the exact malformed line that your code skipped (print it with its line number).
1. Change the parser to also record the earliest and latest timestamp. Paste the code you added and the output.
1. Explain what would happen to your script if the file did not exist, and show the one-line change that would make it fail gracefully.
1. Your instructor changes one field in the file. Re-run and report which count changed. Seed: use the last two digits of your roll number as the number of lines to filter on, and state it.

## Code files in this week

- [`code/example_01.py`](code/example_01.py)
