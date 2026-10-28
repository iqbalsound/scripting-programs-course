# Assignments

[⬅ Assessments index](README.md)


### Assignment 1 (Weeks 1-5), 3 marks, CLO 1

Build a standard-library-only Python script that reads a supplied log (Forensic) or CSV (Cloud) line by line, extracts at least three fields, survives malformed lines, and prints or saves a summary.

1. Read the file line by line (`csv` module for CSV).
1. Extract at least three fields per line (Forensic: timestamp, source IP, event type; Cloud: resource ID, region, status).
1. Handle at least one malformed-line case and report how many were skipped.
1. Summary: counts per event type or per region and status; earliest and latest timestamp (Forensic).
1. Submit the `.py` file, a half-page explanation, and the GitHub link with at least three commits.

| Rubric | Marks |
| --- | --- |
| Correct field extraction and summary output | 1.5 |
| Robust handling of at least one malformed input case | 1 |
| Clarity of the written explanation | 0.5 |

> Personalisation Give each student a different input file by seeding a generator script with the roll number, or ask them to filter on a value derived from it. Two identical submissions then become obvious.


### Assignment 2 (Weeks 6-10), 3 marks, CLO 2 (2) and CLO 3 (1)

Build a Node.js script that fetches JSON from a free public API (Forensic) or from a public API or local emulator (Cloud), with defensive error handling.

1. Use `axios` or built-in `fetch` with a timeout.
1. Parse and display at least two specific fields.
1. Wrap the network call in `try/catch` (or `.catch()`), logging a clear message on failure.
1. Save the data to a local file with a timestamped name.
1. Submit the script and a one-paragraph note on which failure scenario you tested and how it was handled, plus the GitHub link.

| Rubric | Marks |
| --- | --- |
| Correct API call and field extraction | 1.5 |
| Demonstrated, working error handling for at least one failure scenario | 1 |
| Clarity and correctness of the note | 0.5 |


### Assignment 3 (Weeks 11-16), 4 marks, CLO 2 (2) and CLO 3 (2)

Capstone mini-project: containerise one of your earlier scripts, add structured logging and error handling, and build a GitHub Actions workflow that runs on every push.

1. Choose a base script (Assignment 1, Assignment 2 or the Week 11 workflow).
1. Replace all print/console output with Python `logging` or Winston at suitable levels; add at least one specific exception handler.
1. Author a correctly ordered, non-root Dockerfile and `.dockerignore`; confirm build and run locally.
1. Add a GitHub Actions workflow: checkout, install, smoke test, build the image; Week 15 adds the Trivy scan (recommended).
1. Submit the repository link and a README mapping each component to a CLO. The repository must show at least five commits and one reviewed pull request.

| Rubric | Marks |
| --- | --- |
| Correct, working Dockerfile and successful local build/run | 1.5 |
| Appropriate structured logging and at least one handled exception | 1.5 |
| Working CI workflow that runs automatically on push (the commit history and pull-request evidence for CLO 3 are checked here) | 1 |
