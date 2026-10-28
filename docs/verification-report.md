# Lab Manual Verification Report, Fall 2026

Converted from `Lab_Manual_Verification_Report_Fall_2026.docx`.

Hamdard University Karachi

Faculty of Engineering Sciences and Technology

**Lab Manual Verification Report**

Combined Laboratory Manual: DFSP-5208 and CCSP-5213

**Findings, tool checks and repair list**

*Instructor: Iqbal Uddin Khan | Fall 2026*

**Contents**
## 1. Verdict and Method

I re-verified the **Combined Laboratory Manual** (DFSP-5208 Part I and CCSP-5213 Part II, 16 labs each) against three things: the revised Fall 2026 lecture notes, the approved course outlines, and the tools as they stand in October 2026. I also **ran the manual's own code** wherever the sandbox allowed, instead of only reading it.

| Check | How it was done | Result |
| --- | --- | --- |
| Structure | Read all 32 labs for the six-section format, objectives, prerequisites and tasks | Consistent and well organised; free-tool principle respected |
| Code execution | Extracted 147 code blocks; ran the Python, Bash and Node.js labs that need no network or Docker (Labs 1-7, 9-12 logic, 8 handlers, 10 SMTP, 16 data flow) | Defects reproduced by execution: Lab 3 counter, Lab 4 (self-move, overwrite, count), Lab 7 exit code, CCSP Lab 11 retry, CCSP capstone data mismatch |
| Tool currency | Online checks for faasd/OpenFaaS, MinIO and Jenkins; reasoning for MailHog, Node, Python versions | 4 tool problems confirmed |
| Lecture alignment | Mapped each lab to the revised Weeks 1-16 notes | Week numbering is off by one from Lab 9; several Week 10-15 skills are not practised in labs |
| Not verifiable here | Docker, faasd, Jenkins, Trivy, GitHub Actions, public websites/APIs, lnav, nodemailer, winston (no network or daemon in the sandbox) | Reasoned or checked against documentation; marked clearly |


### Overall verdict

The manual is a strong base: it keeps the course on free tools, follows one clear template and builds sensibly from scripting to containers. **It is not ready to hand to students unchanged.** Of 35 findings, **11 are blockers** (a student following the steps exactly will hit a failure or get a wrong result), 12 are major and 12 are minor. The blockers cluster in three places:

- **Wrong or misleading results:** Lab 3 reports "0 rows written" while writing the rows; Lab 4 moves the script itself into the archive.
- **Docker labs (13, 14, 16):** the bind mount `-v $(pwd)/out:/app` hides the application code, so the container fails; Jenkins (Lab 15) has no Docker CLI; the capstone passes the wrong data type between stages.
- **Tools that changed:** faasd Community Edition now carries a non-commercial, personal-use EULA and Lab 8 omits the registry step it needs; MinIO stopped publishing images in October 2025; Jenkins is moving off Java 17.

Section 7 gives a prioritised repair list. The companion file **Lab_Manual_Solutions_Fall_2026.docx** contains corrected, tested code for every lab.


### Legend

| Mark | Meaning |
| --- | --- |
| Executed | The code was run in a sandbox (Python 3.12.3, Node 22, Bash 5.2, Linux) and the behaviour observed |
| Online | Confirmed from current project documentation or announcements |
| Reasoned | Follows from documented behaviour but could not be run here (Docker, Jenkins, faasd) |

| Severity | Meaning |
| --- | --- |
| Blocker | Following the manual exactly fails or gives a wrong result |
| Major | Works but teaches or measures the wrong thing, or is unsafe, outdated or misaligned with the notes |
| Minor | Polish, clarity or small risk |

## 2. Findings

| # | Lab | Sev. | Finding | Status | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | DFSP 1-2, CCSP 1-2 | Blocker | Lab 1 tells Ubuntu 24.04 users to run apt install python3 and "confirm 3.13.x or later". Ubuntu 24.04 ships Python 3.12 (the sandbox, also 24.04, printed 3.12.3), so the required screenshot cannot be produced. | Reasoned + Executed | Require "3.12 or newer". Use 3.13/3.14 only if the lab PC provides it. |
| 2 | DFSP 3, CCSP 3 | Blocker | The CLI prints "0 rows with level=WARN written" while the file contains 23 rows. csv.writer.writerow() returns the number of characters written, so writer.writerow(row) is None is always False and the generator never counts. | Executed | Count in a plain loop (see solution). Also handle missing columns. |
| 3 | DFSP 4, CCSP 4 | Blocker | organize.sh run as ./organize.sh . moves itself into archive_*/other/. A second run then fails with "not found". | Executed | Skip the script's own name. |
| 4 | DFSP 4, CCSP 4 | Major | Summary "Organised 14 items" for 3 files: it counts lines of ls -R output. mv silently overwrites a same-named file already archived, which is a risk for evidence. | Executed | Count per category; rename on a clash. |
| 5 | DFSP 5, CCSP 5 | Major | Backup tars the whole ~/forensic-scripting tree including every .venv (hundreds of MB, every 10 minutes); no checksum; script path ~/lab05/backup.sh does not match the folder created in earlier labs (~/forensic-scripting/lab05). CCSP Lab 5 uses no cloud CLI although the outline lists "Cloud CLI". | Reasoned | Exclude .venv; add SHA-256 and verification; fix path; add --endpoint-url CLI step for Cloud. |
| 6 | DFSP 7, CCSP 7 | Minor | Renamer exits with code 0 when the folder does not exist (.catch(console.error)), has no dry-run, and Node 22 is now in maintenance (Node 24 is the active LTS). | Executed | Exit 1 on error, dry-run by default, "current LTS (22 or 24)". |
| 7 | DFSP 8, CCSP 8 | Blocker | faas-cli up builds and pushes the image. faasd has no built-in registry, and the manual never configures one. The image name ioc-alert:latest cannot be pushed or pulled as written. | Online | Run registry:2 and set the image to 127.0.0.1:5000/..., or use the local harness (Tier 1) as the graded path. |
| 8 | DFSP 8, CCSP 8 | Major | The manual calls OpenFaaS/faasd "fully open source, Apache-2.0". The faasd repository states faasd CE is for non-commercial, personal use only under the faasd CE EULA. Whether a university lab counts needs a decision. faasd also needs Linux with systemd (not plain Windows). | Online | Check the EULA with your department; keep a local-harness option for every student. |
| 9 | DFSP 8, CCSP 8 | Minor | Uses the node20 template; Node 20 reached end of life in April 2026. Docker is installed with curl \\| sudo sh, which is a poor habit in a security course; faasd uses containerd and does not need Docker itself. | Reasoned | Prefer a newer template if available in the template store; show the apt repository method. |
| 10 | DFSP 9, CCSP 9 | Major | Lab 9 fetches jsonplaceholder posts/todos with no key, no timestamped evidence file, no hash, no custody log and no non-200 handling in the code (only raise_for_status). The Week 10 notes require all of these. sqlite3 CLI is used but never installed. | Executed | Replace with the evidence workflow; add apt install sqlite3. |
| 11 | CCSP 9-10 | Major | Cloud labs 9-10 use a to-do list API and a hard-coded vm-01, 72.5. There is no cloud endpoint, so CLO 1 "interact with cloud services" is not practised. | Executed | Use an emulator (Moto) as in the revised notes; read cost from the response. |
| 12 | DFSP 10, CCSP 10 | Major | Lab 10 is one-shot: no SQLite state, no duplicate prevention, no scheduling. Week 11 teaches exactly these. MailHog has had no release since 2020; use Mailpit or aiosmtpd. The CCSP lab says "the budget-check logic from Lab 8", but nothing in Lab 8 is called. | Executed | Add state and scheduler tasks; switch SMTP sink. |
| 13 | DFSP 11, CCSP 11 | Major | Log lines in parse_errors.log have no timestamp (default format, "WARNING:root:..."). messy_log.csv is required but not supplied. No custom exception, pdb, or Git pull-request task, which the Week 12 notes require (CLO 3). | Executed | Supply the file, add a timestamped format, add the Week 12 tasks. |
| 14 | CCSP 11 | Blocker | fetch_with_retry catches the built-in ConnectionError. requests.exceptions.ConnectionError is not a subclass of it (confirmed False; it derives from OSError), so a real network failure is never retried. | Executed | Catch requests.exceptions.RequestException or OSError. |
| 15 | DFSP 12, CCSP 12 | Minor | No console handler, no JSON logging in Python, and no tamper-evidence step (hash a closed log). lnav output cannot be checked by instructors from a screenshot alone. | Executed | Add JSON handler and hash task. |
| 16 | DFSP 13, CCSP 13 | Blocker | docker run -v $(pwd)/out:/app ... bind-mounts a host folder over `/app`, hiding log_filter_cli.py and sample_data.csv that the image contains. The container fails with "can't open file", and out/output.csv is never created. Also the pip install --upgrade pip line is pointless, and the container runs as root. | Reasoned (Docker not available) | Mount a sub-folder: -v "$PWD/out:/app/out" with --output /app/out/output.csv; add a non-root user. |
| 17 | DFSP 14, CCSP 14 | Blocker | Same -v ...:/app bug in the "second host" run (out2). CCSP Step 5 uploads out/output.csv, which Lab 13 never produced. | Reasoned | Same fix; produce the file first. |
| 18 | CCSP 14 | Blocker | MinIO: official Docker images stopped in October 2025, the community repository went to maintenance mode (3 Dec 2025) and has since been reported as archived, and the full community web console was removed earlier in 2025. docker run minio/minio pulls a stale image, and the "MinIO console screenshot" task is not reliable. The Step 6 "download the artefact" objective is never done. | Online | Use Moto server as the S3 endpoint (as in the notes), or build MinIO from source; add the download step. |
| 19 | DFSP 14 | Minor | Claims that Docker Hub free tier limits private image retention; limits are mainly pull-rate and private-repo count. Statement should be verified before it goes into a graded note. | Reasoned | Reword to "pull rate limits and a limited number of private repositories (check current terms)". |
| 20 | DFSP 15, CCSP 15 | Blocker | The Jenkins container mounts /var/run/docker.sock but the official image has no Docker CLI and the jenkins user lacks socket permission, so sh 'docker build' fails with "docker: not found". "Local repository path" for SCM is a host path the container cannot see. No trigger is configured although the objective says "on every commit". | Reasoned | Build a small Jenkins image with the Docker CLI, add the socket group, mount the repository or use GitHub/Gitea, add pollSCM. |
| 21 | DFSP 15, CCSP 15 | Major | jenkins/jenkins:lts-jdk17: Jenkins core 2.545 and later requires JDK 21, and the April 2026 LTS baseline drops Java 17. The lab needs the tag lts-jdk21. The lab has no security scan, although titled "Secure Deployment", and the lecture notes use GitHub Actions with Trivy. | Online | Move to lts-jdk21, add a Trivy stage, offer a GitHub Actions option. |
| 22 | DFSP 16 | Blocker | cp ../lab15/Jenkinsfile fails: the Jenkinsfile was created in lab13. data/raw.csv is never supplied. alert_workflow.py ignores scan_result.json (the IOC list and log line are hard-coded), so stages 2 and 3 are not connected. Inside the container, 127.0.0.1 is the container itself, so curl to faasd fails, and python:slim has no curl. | Executed + Reasoned | Corrected capstone with an alert script that reads the scan result and a SCAN_URL setting. |
| 23 | CCSP 16 | Blocker | The pipeline posts a CSV of log rows with Content-Type: application/json to usage-alert, which runs JSON.parse(body). Confirmed: it throws "Unexpected token 'i'... is not valid JSON". scripts/upload_to_minio.py is never created. alert_workflow.py is the hard-coded vm-01 / 72.5 demo. | Executed | Convert each row to JSON; add the upload script (Moto endpoint). |
| 24 | All | Major | Labs 9-16 are labelled Week 9-16, but Week 9 is the midterm and the revised Weeks 10-15 cover the same content one week later. The outline lab table has the same offset. Lab 14 and Lab 15 both land in Week 15. | Executed (cross-check) | Use the mapping in Section 5. |
| 25 | All | Major | Instructions are Linux-only (source, ~, $(pwd), sudo apt, cron) but the prerequisites say Windows 11 is fine. Only Lab 4 mentions WSL2, and service cron start needs systemd in WSL. | Reasoned | State "Windows students must use WSL2 with systemd" in the introduction and add a PowerShell column for the few commands that differ. |
| 26 | All | Major | Several labs install tools with curl ... \\| sudo sh (Docker, NodeSource, faas-cli). Students are taught to run unreviewed remote scripts as root in a security course. | Reasoned | Use the package manager repository method, or download, inspect and then run. |
| 27 | All | Minor | Timestamps use datetime.now() (local, naive) in Labs 2 and others; the notes require UTC. random without a seed means each student has different data, which makes checking answers harder. | Executed | Use timezone-aware UTC and random.seed(42). |
| 28 | All | Minor | The manual says "Python 3.13 / Node.js 22 are the latest stable". In October 2026 Python 3.14 is out and Node 24 is the active LTS. "Latest" claims age quickly. | Reasoned | State a minimum version rather than "latest". |
| 29 | DFSP 6, CCSP 6 | Minor | time.sleep(0.2) is inside the loop over already-downloaded items, so it does not rate-limit anything (one request is made). column -s, breaks on titles containing commas. The lab scrapes a bookshop; the notes mention threat feeds and status pages. | Executed | Put the pause between requests; offer a threat-feed or status-feed option. |
| 30 | CCSP 2-3, 6-7 | Major | Labs 2, 3, 6, 7 are copies of the forensic labs with the nouns swapped. They still process a log-level CSV and a bookshop page. Assessments (Assignment 1) use resources.csv (id, region, status). | Reasoned | Give CCSP a resources dataset and a status-page/RSS target. |
| 31 | Both | Minor | Dates and calendar items are absent, and Required Outcomes ask for screenshots only. Screenshots are easy to share; the notes require a system clock and a personal seed. | Reasoned | Add "system clock visible" and one personalised parameter per lab. |
| 32 | DFSP 12 | Minor | Winston rotation task says to use winston-daily-rotate-file; Winston's own File transport already supports maxsize and maxFiles, which is enough for the "no file over 1 MB" requirement. | Reasoned | Accept either; the solution shows the built-in option. |
| 33 | Both 8 | Minor | Prerequisite chain: Lab 8 requires Docker, but Docker is taught in Lab 13. The manual installs it in Lab 8 "minimally" and again in Lab 13. | Reasoned | Install Docker once in Lab 1 setup. |
| 34 | Both | Minor | No lab practises Git collaboration (branch, pull request, review) although CLO 3 requires it; Git first appears in Lab 15. | Reasoned | Add a Git task in Labs 3, 7, 11 and 15. |
| 35 | Both 15-16 | Minor | The lecture notes use GitHub Actions and Trivy; the manual uses Jenkins. Both are free, but students need one route that matches the exam and Assignment 3. | Reasoned | Make GitHub Actions the primary and Jenkins an optional extension (or the reverse, but state it). |

Counts: Blockers = 11, Major = 12, Minor = 12.

## 3. Tool and Version Verification

| Tool in manual | Manual says | Status in October 2026 | Action |
| --- | --- | --- | --- |
| Python 3.13 | Latest stable | 3.14 is current; 3.13 is supported. Ubuntu 24.04 apt gives 3.12 | Minimum 3.12 |
| Node.js 22 LTS | LTS | Node 24 is active LTS; 22 is in maintenance (Online/Reasoned) | State "current LTS (22 or 24)" |
| OpenFaaS + faasd | Apache-2.0, fully open source | faasd CE is non-commercial, personal use under an EULA; needs a registry (Online) | Confirm EULA suits a class; add registry step or local harness |
| node20 template | Used for functions | Node 20 is end-of-life since April 2026 (Reasoned) | Use a newer template if available |
| MailHog | Free OSS SMTP test server | Unmaintained since 2020 (Reasoned); still works for demos | Prefer Mailpit or aiosmtpd |
| Docker Engine CE | Free, Apache-2.0 | Correct; Docker Desktop terms are separate | No change |
| registry:2 | Self-hosted registry | Works; a newer major version also exists (Reasoned) | No change needed for the lab |
| MinIO | Free, runs from minio/minio | Images stopped Oct 2025; maintenance mode Dec 2025; reported archived Feb 2026 (Online) | Replace with Moto S3 endpoint |
| Jenkins lts-jdk17 | Official LTS image | Core 2.545+ requires JDK 21; LTS baseline from April 2026 drops Java 17 (Online) | Use lts-jdk21 |
| Winston, Nodemailer, axios | npm packages | Current, free (not run here) | No change |
| lnav | Log viewer | Available in Ubuntu repositories (not run here) | No change |
| jsonplaceholder.typicode.com | Public test API | A third-party site; availability not guaranteed | Offer the local mock API as fallback |
| books.toscrape.com | Scraping sandbox | Third-party site built for practice (not run here) | Offer a local test page as fallback |

## 4. Alignment with the Revised Lecture Notes


### Lab-to-week mapping (recommended)

| Manual lab | Manual label | Teach in lecture week | Notes |
| --- | --- | --- | --- |
| Lab 1 | Week 1 | Week 1 |  |
| Lab 2 | Week 2 | Week 2 | Add exception primer |
| Lab 3 | Week 3 | Week 3 | Add logging primer and Git basics |
| Lab 4 | Week 4 | Week 4 |  |
| Lab 5 | Week 5 | Week 5 | Add exit codes |
| Lab 6 | Week 6 | Week 6 |  |
| Lab 7 | Week 7 | Week 7 | Add pull request |
| Lab 8 | Week 8 | Week 8 | Local-first tiers |
| (none) | Week 9 = midterm | Week 9 | No lab |
| Lab 9 | Week 9 | Week 10 | REST/JSON |
| Lab 10 | Week 10 | Week 11 | Workflow |
| Lab 11 | Week 11 | Week 12 | Errors and debugging |
| Lab 12 | Week 12 | Week 13 | Logging |
| Lab 13 | Week 13 | Week 14 | Docker |
| Lab 14 | Week 14 | Week 14 (second half) or Week 15 | Registry; two labs share a week |
| Lab 15 | Week 15 | Week 15 | CI/CD |
| Lab 16 | Week 16 | Week 16 | Capstone |


### Skills in the revised notes that no lab currently practises

| Week | Skill in notes | Lab coverage | Add to |
| --- | --- | --- | --- |
| 10 | API key from .env, status codes, timestamped evidence file, SHA-256, custody log, 429 rate limit | None (public API without key) | Lab 9 |
| 10 | Node.js fetch parity (Assignment 2) | axios only; no error branch | Lab 9 |
| 11 | SQLite dedupe, idempotency, scheduler | None | Lab 10 |
| 12 | pdb, custom exceptions, traceback capture, pull-request review | VS Code debugger only | Lab 11 |
| 13 | JSON log lines, rotation test, hash of closed log, retention policy | Rotation and Winston only | Lab 12 |
| 14 | --env-file, non-root user, cache ordering test, .dockerignore proof | Not covered; bind-mount bug | Lab 13 |
| 15 | Pinned actions, permissions, Trivy gate, branch protection | Jenkins without scan | Lab 15 |
| 1-8 | Git (CLO 3) | First used in Lab 15 | Labs 1, 3, 7 |
| 5 | Cloud CLI against an endpoint (outline lab table) | Not used | CCSP Lab 5 |


### Consistency with the assessment pack

- Assignment 1 expects `auth.log` (Forensic) and `resources.csv` (Cloud); Labs 2-3 use a generic `timestamp,host,level,message` CSV. Either align the assessment inputs with the lab data, or ship both generators.
- The class task (Week 8) assumes exception handling, logging and Git primers; those are now in the solution versions of Labs 2, 3 and 7.
- Assignment 3 asks for a Dockerfile, logging and GitHub Actions; Lab 15 should therefore include the GitHub Actions path.

## 5. Lab-by-Lab Status

| Lab | Topic | DFSP | CCSP | Must-fix before use |
| --- | --- | --- | --- | --- |
| 1 | Python intro | Fix | Fix | Python version claim (finding 1) |
| 2 | File handling | OK* | Fix | *UTC and seed; CCSP dataset (30) |
| 3 | argparse CLI | Blocker | Blocker | Row counter prints 0 (2) |
| 4 | Bash basics | Blocker | Blocker | Script moves itself (3) |
| 5 | cron backup | Fix | Fix | .venv in backup, path, cloud CLI (5) |
| 6 | Scraping | OK* | Fix | *Rate-limit placement (29) |
| 7 | Node.js files | OK* | OK* | *Exit code, dry-run (6) |
| 8 | Serverless | Blocker | Blocker | Registry step, faasd EULA (7, 8) |
| 9 | REST/JSON | Fix | Fix | No evidence workflow (10, 11) |
| 10 | Workflow/alerts | Fix | Fix | No state or scheduler (12) |
| 11 | Errors/debug | Fix | Blocker | CCSP retry catches wrong exception (14) |
| 12 | Logging | OK* | OK* | *JSON and hash tasks (15) |
| 13 | Docker | Blocker | Blocker | Bind mount hides /app (16) |
| 14 | Registry / storage | Blocker | Blocker | Same mount bug; MinIO (17, 18) |
| 15 | CI/CD | Blocker | Blocker | No Docker CLI in Jenkins (20, 21) |
| 16 | Capstone | Blocker | Blocker | Stages not connected (22, 23) |

## 6. What Is Good and Should Stay

- The six-section template (title, objectives, theory, prerequisites, steps, outcomes) is clear and matches the course style.
- The free-and-open-source stance is applied consistently, and every lab states how it avoids a paid account.
- Safe synthetic data is used (no real evidence); the scraping lab names `robots.txt` and rate limiting.
- Good touches: `set -euo pipefail` with an explanation, `.gitignore` for `.venv`, parametrised SQL (`?`) in Lab 9, `timeout=` on requests, `INSERT OR REPLACE`, `fs/promises` in Node, logging rotation parameters.
- The capstone design (diagram, orchestration script, container, CI) is the right shape; it only needs the connections repaired.

## 7. Prioritized Repair List


### Priority 1: before Week 1 (blockers)

1. Lab 1: change "Python 3.13" to "3.12 or newer" in the steps, the tool table and the screenshot task.
1. Lab 3: replace the counter line with a plain loop (see solution).
1. Lab 4: skip the script's own file and print per-category counts.
1. Labs 13, 14, 16: mount `-v "$PWD/out:/app/out"` and write to `/app/out/...`; stop mounting over `/app`.
1. Lab 15: build the Jenkins image with the Docker CLI (or choose GitHub Actions as primary); use `lts-jdk21`.
1. Lab 8: decide on the serverless route. Make the local harness the graded path, keep faasd as optional with a registry step, and check the EULA.
1. CCSP Lab 11: catch `requests.exceptions.RequestException`.
1. CCSP Lab 14: use Moto as the S3 endpoint; remove MinIO console tasks.
1. Lab 16: connect the stages (alert script reads the scan result, JSON conversion for the Cloud function, `SCAN_URL` setting, missing files supplied).


### Priority 2: before the lab that uses them

1. Labs 9-10: switch to the evidence workflow, add state, scheduling and a local mock API.
1. Labs 11-12: add `pdb`, custom exception, Git pull-request, JSON logging and hash tasks.
1. Lab 5: exclude `.venv`, add checksum, add the cloud CLI step for CCSP.
1. Windows note and PowerShell equivalents; replace `curl | sh` installs.


### Priority 3: polish

1. UTC timestamps and seeded random data.
1. Add "system clock visible" and a personal seed to each Required Outcomes list.
1. Replace "latest" with minimum versions.
1. CCSP datasets and targets that look like cloud data.

## 8. Limits of This Verification

- The sandbox had no Docker daemon, no internet and no Jenkins, so Labs 8 (faasd), 13, 14, 15 and the Docker parts of 16 were **reasoned from documentation** , not run. The bind-mount behaviour and the missing Docker CLI in the Jenkins image are standard, well-documented behaviours, but please run Labs 13 and 15 once on a lab PC before term.
- Public sites (jsonplaceholder, books.toscrape.com) and packages (axios, nodemailer, winston, lnav) were not reachable, so those labs were tested against a local mock server or by reading the code.
- Version and licence statements for faasd, MinIO and Jenkins come from current project pages found during this review. Re-check them just before term because they can change again.
