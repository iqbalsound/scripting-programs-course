# Quizzes (with model answers)

[⬅ Assessments index](README.md)

All instruments follow the approved marks distribution (Section 2). Questions are written so that a correct answer needs a **personal artefact** (own output, own hash, own repository), which also addresses the academic-integrity expectations in the outlines. Model answers are given for quick marking.


## Quiz 1 (Weeks 1-5), 3 marks, closed book, 15 minutes

| Q | Question | CLO | Marks |
| --- | --- | --- | --- |
| 1 | In one or two sentences, distinguish scripting from compiled programming. Give one automation example of each for your track (forensic: log triage vs a custom disk-imaging tool; cloud: bucket sync vs a custom storage engine). | 1 | 1 |
| 2 | Write the exact output of the snippet below. | 1 | 1 |
| 3 | Describe one realistic task that needs both a Python script and a Bash script in your track's pipeline. State what each script does and how they communicate (exit code, file, pipe). | 2 | 1 |

```python
files = ["a.log", "b.txt", "c.log"]
for f in files:
    if f.endswith(".log"):
        print("parse", f)
    else:
        print("skip", f)
```

**Model answers:** Q1: interpreted, quick to change, glue code, versus compiled for performance and large systems (0.5 for definition, 0.5 for valid example). Q2: `parse a.log`, `skip b.txt`, `parse c.log` (each on its own line). Q3: for example, Bash `cron` runs a Python parser and uses its exit code to decide whether to upload the report (0.5 for task, 0.5 for the interface between them).


## Quiz 2 (Weeks 6-10), 3 marks, closed book, 15 minutes

| Q | Question | CLO | Marks |
| --- | --- | --- | --- |
| 1 | Forensic: why is Node.js well suited to renaming thousands of evidence files? Cloud: why is Node.js well suited to a serverless function? Answer in two sentences. | 2 | 1 |
| 2 | List, in order, the steps a script takes to retrieve JSON from a REST API and store it safely (include at least five steps). | 2 | 1 |
| 3 | Identify the defect in the snippet below and give the one-line fix. | 3 | 1 |

```python
resp = requests.get(url, headers=headers)
data = resp.json()
print(data["data"]["score"])
```

**Model answers:** Q1: non-blocking I/O with async/await handles many file operations concurrently; small, event-driven handlers fit serverless. Q2: load credential from environment, send request with timeout, catch network exceptions, check status code, parse JSON defensively, write timestamped file, hash it, log it. Q3: no timeout and no status check, so an error body is parsed as data; fix: `resp = requests.get(url, headers=headers, timeout=10); resp.raise_for_status()` (also accept a `.get()` based fix for missing keys).


## Quiz 3 (Weeks 11-15), 4 marks, closed book, 20 minutes

| Q | Question | CLO | Marks |
| --- | --- | --- | --- |
| 1 | Give the correct order of instructions in a minimal Dockerfile for a Python script and explain in one sentence why dependency installation precedes the code copy. | 2 | 1 |
| 2 | Name one free, open-source tool that scans a container image for known vulnerabilities in a CI pipeline, and say what policy you would make it enforce. | 2 | 1 |
| 3 | Forensic: the function below opens an evidence file. Cloud: the function below calls a cloud API. Name the specific exception to catch and show the except line. | 3 | 1 |
| 4 | Why is a rotating file handler preferable to an unbounded log file in a long-running monitor? Give one further reason to keep a retention policy. | 3 | 1 |

```python
# Forensic version
def load(path):
    with open(path) as f:
        return f.read()

# Cloud version
def status(url):
    return requests.get(url, timeout=10).json()
```

**Model answers:** Q1: FROM, WORKDIR, COPY requirements, RUN pip install, COPY code, (USER), ENTRYPOINT; caching means code edits do not reinstall dependencies. Q2: Trivy (or Grype); fail the build on HIGH/CRITICAL fixable findings. Q3: `except FileNotFoundError` (or `OSError`), `except requests.exceptions.RequestException`. Q4: caps disk use and keeps files manageable; retention balances evidential or diagnostic value against storage and privacy.
