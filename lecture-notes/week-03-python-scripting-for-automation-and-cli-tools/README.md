# Week 3: Python Scripting for Automation and CLI Tools

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 1 (Apply) | Sweigart, Automate the Boring Stuff, Ch. 9 (files) | argparse log or CSV tool |

> Revised for Fall 2026 New: logging primer (10 minutes, logging.basicConfig, replacing print) and Git basics (commit, branch, push to GitHub) so students can meet Assignment 1 and the class task expectations.


### Learning objectives

- Read and write text, CSV and JSON files.
- Build a command-line tool with `argparse`.
- Replace `print` with basic logging; push work to GitHub.


### Hour 1: File handling

- `open()` with context managers; text vs binary; encodings.
- `csv.DictReader`, `json.load`/`json.dump`.
- Why not to hard-code paths: use arguments.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Automate parsing of authentication logs and writing a JSON summary.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Automate reading and updating a cloud configuration JSON file.


### Hour 2: Command-line tools

- `argparse`: positional arguments, options, `--help`, defaults, `choices`.
- Exit codes: `sys.exit(0)` for success and non-zero for failure; this matters for Bash and CI later.

```python
import argparse, sys
p = argparse.ArgumentParser(description="Summarise a log file")
p.add_argument("path")
p.add_argument("--top", type=int, default=5, help="how many items to show")
args = p.parse_args()
print(f"Reading {args.path}, top {args.top}")
```

> 📁 Saved as [`code/example_01.py`](code/example_01.py)


### Hour 3: Practical and Git

- Lab: finish the CLI tool; add `--output` to write the summary to a file.
- Logging primer: `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")`; use `logging.warning` for skipped lines.
- Git: `git add`, `git commit`, `git remote add origin`, `git push`. Every student pushes their lab.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalized, see the Appendix on personalization.

1. Run `python tool.py --help` and paste the exact output.
1. Run the tool with `--top` set to your seed (last digit of your roll number, minimum 3). Paste output and command.
1. Paste the log lines your tool produced at WARNING level for malformed input.
1. Share the URL of your GitHub repository and paste `git log --oneline` showing at least three commits made this week.
1. Run the tool on a non-existent file and paste what happens. Describe the change needed so that it exits with code 1 and a clear message.

## Code files in this week

- [`code/example_01.py`](code/example_01.py)
