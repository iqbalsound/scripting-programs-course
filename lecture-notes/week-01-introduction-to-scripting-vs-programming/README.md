# Week 1: Introduction to Scripting vs Programming

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 1 (Apply) | Sweigart, Automate the Boring Stuff, Ch. 1 | Hello Security / Hello Cloud script |


### Learning objectives

- Distinguish scripting from compiled programming and say when each is the right tool.
- Explain why automation reduces human error and improves repeatability in security and cloud operations.
- Set up a working environment (Python, VS Code, Git) and run a first script.


### Hour 1: Conceptual foundations

- **Scripting vs compiled programming:** scripts are interpreted line by line and optimized for glue work and quick change; compiled languages (C++, Java) are built into binaries for performance and large systems. The line is blurry (Python compiles to bytecode), so teach it as a *purpose* distinction.
- **Why automate:** consistency, speed, auditability, and removal of copy-paste error. A manual step done 500 times will eventually be done wrongly once.
- **Case study:** an analyst parsing thousands of log lines after a breach versus an engineer scripting nightly backups.


### Hour 2: Applications in security and cloud

- Digital forensics: log parsing, hashing evidence, malware triage, timeline building.
- Cloud: provisioning, snapshots, API integration, cost and capacity checks.
- DevOps and incident response: the same script runs the same way every time, which is the foundation of Weeks 14-15.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Show a 6-line script that hashes every file in a folder. Explain that identical hashes before and after a copy are the evidence-integrity check used throughout the course.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Show the same loop listing the objects in a storage bucket. Explain that the loop is identical, only the data source changes.


### Hour 3: Practical orientation

- Demo: `print("Hello Security")` / `print("Hello Cloud")`, running from terminal and from VS Code.
- Create a project folder, a virtual environment and a Git repository (`git init`, first commit). Explain that every later lab is committed.
- Discussion: where would a script beat a GUI in your own daily work?

```python
import platform, datetime, hashlib, pathlib
me = pathlib.Path(__file__).read_bytes()
print("Host :", platform.node())
print("UTC  :", datetime.datetime.now(datetime.timezone.utc).isoformat())
print("SHA256 of this script:", hashlib.sha256(me).hexdigest())
```

> 📁 Saved as [`code/example_01.py`](code/example_01.py)


### Step-by-step lab method (free and open-source tools only)

1. Install Python, VS Code and Git; confirm `python --version` and `git --version`.
1. Create `week01/`, a venv, and `git init`.
1. Save the script above as `hello.py` and run it twice, editing one character in between.
1. Observe that the hash changes; commit both versions with meaningful messages.
1. Take a screenshot showing the terminal and the system clock.


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalized, see the Appendix on personalization.

1. Run `hello.py` and paste the exact output. State your machine name and UTC time as printed.
1. Edit one character of the script and paste both SHA-256 values. Explain in one sentence what this shows about integrity checking.
1. Show `git log --oneline` from your repository with at least two commits.
1. Describe one repetitive task from your own life or lab that you would script first, and write the first three steps as pseudo-code.
1. In two sentences, argue for a script or a compiled program for a tool that must scan 10 GB of logs in under a minute. Defend the trade-off.

## Code files in this week

- [`code/example_01.py`](code/example_01.py)
