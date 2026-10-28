# Changelog

All notable changes between the **original combined lab manual** and the **Fall 2026 revised edition**, extracted from the *Lab Manual Verification Report* (findings, severity, how each was verified, recommended fix) and cross-referenced with the change log printed at the end of the revised manual (what was actually changed).

> **Review result:** 35 findings. Blocker: 11, Major: 12, Minor: 12 (counted from the table below). A *blocker* means a student following the steps exactly hits a failure or a wrong result.

Verification marks: **Executed** = code was run in a sandbox (Python 3.12.3, Node 22, Bash 5.2); **Online** = confirmed from current project documentation; **Reasoned** = follows from documented behaviour but could not be run (Docker, Jenkins, faasd).

## [Fall 2026 Revised Edition]

### Fixed: blockers

| # | Lab(s) | Severity | Finding (verification report) | How verified | Recommended fix | Change made in the revised manual |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | DFSP 1-2, CCSP 1-2 | Blocker | Lab 1 tells Ubuntu 24.04 users to run apt install python3 and "confirm 3.13.x or later". Ubuntu 24.04 ships Python 3.12 (the sandbox, also 24.04, printed 3.12.3), so the required screenshot cannot be produced. | Reasoned + Executed | Require "3.12 or newer". Use 3.13/3.14 only if the lab PC provides it. | Python requirement changed from “3.13 or later” to “3.12 or newer” in the steps, tool table, prerequisites and the screenshot task. |
| 2 | DFSP 3, CCSP 3 | Blocker | The CLI prints "0 rows with level=WARN written" while the file contains 23 rows. csv.writer.writerow() returns the number of characters written, so writer.writerow(row) is None is always False and the generator never counts. | Executed | Count in a plain loop (see solution). Also handle missing columns. | log_filter_cli.py now counts written rows in a plain loop, handles a missing column, reports missing input with exit code 1, and gains --limit and timestamped logging. |
| 3 | DFSP 4, CCSP 4 | Blocker | organize.sh run as ./organize.sh . moves itself into archive_*/other/. A second run then fails with "not found". | Executed | Skip the script's own name. | organize.sh skips its own file name, so it no longer moves itself and a second run works. |
| 7 | DFSP 8, CCSP 8 | Blocker | faas-cli up builds and pushes the image. faasd has no built-in registry, and the manual never configures one. The image name ioc-alert:latest cannot be pushed or pulled as written. | Online | Run registry:2 and set the image to 127.0.0.1:5000/..., or use the local harness (Tier 1) as the graded path. | Lab 8 split into Tier 1 (local harness, graded) and Tier 2 (faasd); Tier 2 now starts registry:2 and uses a 127.0.0.1:5000 image name. |
| 14 | CCSP 11 | Blocker | fetch_with_retry catches the built-in ConnectionError. requests.exceptions.ConnectionError is not a subclass of it (confirmed False; it derives from OSError), so a real network failure is never retried. | Executed | Catch requests.exceptions.RequestException or OSError. | Retry helper catches OSError / requests.exceptions.RequestException instead of the built-in ConnectionError, with a one-line proof. |
| 16 | DFSP 13, CCSP 13 | Blocker | docker run -v $(pwd)/out:/app ... bind-mounts a host folder over `/app`, hiding log_filter_cli.py and sample_data.csv that the image contains. The container fails with "can't open file", and out/output.csv is never created. Also the pip install --upgrade pip line is pointless, and the container runs as root. | Reasoned (Docker not available) | Mount a sub-folder: -v "$PWD/out:/app/out" with --output /app/out/output.csv; add a non-root user. | Bind mount changed to -v "$PWD/out:/app/out" with output in /app/out; non-root user, .dockerignore added; pointless pip upgrade removed. |
| 17 | DFSP 14, CCSP 14 | Blocker | Same -v ...:/app bug in the "second host" run (out2). CCSP Step 5 uploads out/output.csv, which Lab 13 never produced. | Reasoned | Same fix; produce the file first. | Second-host run mounts out2:/app/out; CCSP Lab 14 first checks that out/output.csv exists. |
| 18 | CCSP 14 | Blocker | MinIO: official Docker images stopped in October 2025, the community repository went to maintenance mode (3 Dec 2025) and has since been reported as archived, and the full community web console was removed earlier in 2025. docker run minio/minio pulls a stale image, and the "MinIO console screenshot" task is not reliable. The Step 6 "download the artefact" objective is never done. | Online | Use Moto server as the S3 endpoint (as in the notes), or build MinIO from source; add the download step. | MinIO replaced by the Moto S3 emulator; console screenshot replaced by list_objects_v2 output; download and cmp step added. |
| 20 | DFSP 15, CCSP 15 | Blocker | The Jenkins container mounts /var/run/docker.sock but the official image has no Docker CLI and the jenkins user lacks socket permission, so sh 'docker build' fails with "docker: not found". "Local repository path" for SCM is a host path the container cannot see. No trigger is configured although the objective says "on every commit". | Reasoned | Build a small Jenkins image with the Docker CLI, add the socket group, mount the repository or use GitHub/Gitea, add pollSCM. | Jenkins image built with the Docker CLI; socket group added; lab13 repository mounted at /repo; pollSCM trigger added. |
| 22 | DFSP 16 | Blocker | cp ../lab15/Jenkinsfile fails: the Jenkinsfile was created in lab13. data/raw.csv is never supplied. alert_workflow.py ignores scan_result.json (the IOC list and log line are hard-coded), so stages 2 and 3 are not connected. Inside the container, 127.0.0.1 is the container itself, so curl to faasd fails, and python:slim has no curl. | Executed + Reasoned | Corrected capstone with an alert script that reads the scan result and a SCAN_URL setting. | Jenkinsfile copied from lab13; raw.csv supplied; alert_from_scan.py reads the scan result; SCAN_URL and host.docker.internal replace 127.0.0.1; curl installed in the image. |
| 23 | CCSP 16 | Blocker | The pipeline posts a CSV of log rows with Content-Type: application/json to usage-alert, which runs JSON.parse(body). Confirmed: it throws "Unexpected token 'i'... is not valid JSON". scripts/upload_to_minio.py is never created. alert_workflow.py is the hard-coded vm-01 / 72.5 demo. | Executed | Convert each row to JSON; add the upload script (Moto endpoint). | Each row is converted to JSON and sent separately; upload_to_s3.py provided; budgets come from the data, not a hard-coded demo. |

### Fixed: major

| # | Lab(s) | Severity | Finding (verification report) | How verified | Recommended fix | Change made in the revised manual |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | DFSP 4, CCSP 4 | Major | Summary "Organised 14 items" for 3 files: it counts lines of ls -R output. mv silently overwrites a same-named file already archived, which is a risk for evidence. | Executed | Count per category; rename on a clash. | Summary counts per category (logs, csv, other); name clashes keep both copies by prefixing the time. |
| 5 | DFSP 5, CCSP 5 | Major | Backup tars the whole ~/forensic-scripting tree including every .venv (hundreds of MB, every 10 minutes); no checksum; script path ~/lab05/backup.sh does not match the folder created in earlier labs (~/forensic-scripting/lab05). CCSP Lab 5 uses no cloud CLI although the outline lists "Cloud CLI". | Reasoned | Exclude .venv; add SHA-256 and verification; fix path; add --endpoint-url CLI step for Cloud. | backup.sh excludes .venv and node_modules, writes and verifies SHA-256, applies 7-day retention; script path corrected to ~/<project>/lab05; CCSP Lab 5 gains the Moto + aws CLI step. |
| 8 | DFSP 8, CCSP 8 | Major | The manual calls OpenFaaS/faasd "fully open source, Apache-2.0". The faasd repository states faasd CE is for non-commercial, personal use only under the faasd CE EULA. Whether a university lab counts needs a decision. faasd also needs Linux with systemd (not plain Windows). | Online | Check the EULA with your department; keep a local-harness option for every student. | Removed the claim that OpenFaaS/faasd is Apache-2.0 and fully open source; faasd CE EULA and the systemd requirement are stated; the harness works for every student. |
| 10 | DFSP 9, CCSP 9 | Major | Lab 9 fetches jsonplaceholder posts/todos with no key, no timestamped evidence file, no hash, no custody log and no non-200 handling in the code (only raise_for_status). The Week 10 notes require all of these. sqlite3 CLI is used but never installed. | Executed | Replace with the evidence workflow; add apt install sqlite3. | Evidence workflow: status check, timestamped evidence file, SHA-256, custody log, .env key and 429 handling task, sqlite3 installed; local mock API added as fallback. |
| 11 | CCSP 9-10 | Major | Cloud labs 9-10 use a to-do list API and a hard-coded vm-01, 72.5. There is no cloud endpoint, so CLO 1 "interact with cloud services" is not practised. | Executed | Use an emulator (Moto) as in the revised notes; read cost from the response. | Moto emulator step added to Lab 9 (cloud-state JSON saved as evidence). Not done: Lab 10 still uses a fixed five- resource list rather than reading costs from the emulator (see Open items). |
| 12 | DFSP 10, CCSP 10 | Major | Lab 10 is one-shot: no SQLite state, no duplicate prevention, no scheduling. Week 11 teaches exactly these. MailHog has had no release since 2020; use Mailpit or aiosmtpd. The CCSP lab says "the budget-check logic from Lab 8", but nothing in Lab 8 is called. | Executed | Add state and scheduler tasks; switch SMTP sink. | MailHog replaced by Mailpit or aiosmtpd; SQLite state and a cron schedule added; CCSP theory no longer says Lab 8 logic is called. |
| 13 | DFSP 11, CCSP 11 | Major | Log lines in parse_errors.log have no timestamp (default format, "WARNING:root:..."). messy_log.csv is required but not supplied. No custom exception, pdb, or Git pull-request task, which the Week 12 notes require (CLO 3). | Executed | Supply the file, add a timestamped format, add the Week 12 tasks. | messy_log.csv / messy_billing.csv supplied; timestamped log format; custom exception, pdb and a Git pull-request task added. |
| 21 | DFSP 15, CCSP 15 | Major | jenkins/jenkins:lts-jdk17: Jenkins core 2.545 and later requires JDK 21, and the April 2026 LTS baseline drops Java 17. The lab needs the tag lts-jdk21. The lab has no security scan, although titled "Secure Deployment", and the lecture notes use GitHub Actions with Trivy. | Online | Move to lts-jdk21, add a Trivy stage, offer a GitHub Actions option. | Jenkins tag changed to lts-jdk21; Trivy scan stage added; GitHub Actions route added. |
| 24 | All | Major | Labs 9-16 are labelled Week 9-16, but Week 9 is the midterm and the revised Weeks 10-15 cover the same content one week later. The outline lab table has the same offset. Lab 14 and Lab 15 both land in Week 15. | Executed (cross-check) | Use the mapping in Section 5. | Lab week labels corrected (Labs 9–16 follow the midterm) and a mapping table added to How to Use This Manual. |
| 25 | All | Major | Instructions are Linux-only (source, ~, $(pwd), sudo apt, cron) but the prerequisites say Windows 11 is fine. Only Lab 4 mentions WSL2, and service cron start needs systemd in WSL. | Reasoned | State "Windows students must use WSL2 with systemd" in the introduction and add a PowerShell column for the few commands that differ. | Windows students are told to use WSL2 with systemd; PowerShell differences noted for venv activation and Docker mounts. |
| 26 | All | Major | Several labs install tools with curl ... \\| sudo sh (Docker, NodeSource, faas-cli). Students are taught to run unreviewed remote scripts as root in a security course. | Reasoned | Use the package manager repository method, or download, inspect and then run. | curl \| sh installs removed: Docker via apt, Node.js via snap or a downloaded and inspected script, faas-cli downloaded and read. |
| 30 | CCSP 2-3, 6-7 | Major | Labs 2, 3, 6, 7 are copies of the forensic labs with the nouns swapped. They still process a log-level CSV and a bookshop page. Assessments (Assignment 1) use resources.csv (id, region, status). | Reasoned | Give CCSP a resources dataset and a status-page/RSS target. | Partly done: resources.csv generator added to CCSP Lab 2 and cloud wording kept; Labs 3, 6 and 7 still share code with Part I (see Open items). |

### Fixed: minor

| # | Lab(s) | Severity | Finding (verification report) | How verified | Recommended fix | Change made in the revised manual |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | DFSP 7, CCSP 7 | Minor | Renamer exits with code 0 when the folder does not exist (.catch(console.error)), has no dry-run, and Node 22 is now in maintenance (Node 24 is the active LTS). | Executed | Exit 1 on error, dry-run by default, "current LTS (22 or 24)". | Renamer is a dry run unless --apply is given, never overwrites, exits with code 1 on error; Node “22 or 24”. |
| 9 | DFSP 8, CCSP 8 | Minor | Uses the node20 template; Node 20 reached end of life in April 2026. Docker is installed with curl \\| sudo sh, which is a poor habit in a security course; faasd uses containerd and does not need Docker itself. | Reasoned | Prefer a newer template if available in the template store; show the apt repository method. | Template choice no longer fixed to node20 (end of life); faas-cli installer is downloaded and read before running; Docker comes from apt (Lab 1). |
| 15 | DFSP 12, CCSP 12 | Minor | No console handler, no JSON logging in Python, and no tamper-evidence step (hash a closed log). lnav output cannot be checked by instructors from a screenshot alone. | Executed | Add JSON handler and hash task. | JSON handler, console handler and a hash-of-closed-log tamper-evidence step added; lnav filter keys corrected. |
| 19 | DFSP 14 | Minor | Claims that Docker Hub free tier limits private image retention; limits are mainly pull-rate and private-repo count. Statement should be verified before it goes into a graded note. | Reasoned | Reword to "pull rate limits and a limited number of private repositories (check current terms)". | Docker Hub wording changed to pull-rate limits and a limited number of private repositories (check current terms). |
| 27 | All | Minor | Timestamps use datetime.now() (local, naive) in Labs 2 and others; the notes require UTC. random without a seed means each student has different data, which makes checking answers harder. | Executed | Use timezone-aware UTC and random.seed(42). | UTC timestamps and random.seed(42) in the generators and scripts. |
| 28 | All | Minor | The manual says "Python 3.13 / Node.js 22 are the latest stable". In October 2026 Python 3.14 is out and Node 24 is the active LTS. "Latest" claims age quickly. | Reasoned | State a minimum version rather than "latest". | “Latest stable” wording replaced by minimum versions in the cover note, tool table and labs. |
| 29 | DFSP 6, CCSP 6 | Minor | time.sleep(0.2) is inside the loop over already-downloaded items, so it does not rate-limit anything (one request is made). column -s, breaks on titles containing commas. The lab scrapes a bookshop; the notes mention threat feeds and status pages. | Executed | Put the pause between requests; offer a threat-feed or status-feed option. | Pause moved between requests; column -s, removed; local test page added; feed-first guidance added. |
| 31 | Both | Minor | Dates and calendar items are absent, and Required Outcomes ask for screenshots only. Screenshots are easy to share; the notes require a system clock and a personal seed. | Reasoned | Add "system clock visible" and one personalised parameter per lab. | Every outcomes list asks for the system clock in screenshots; personal values added (roll number in Lab 1, budget in CCSP Lab 10). |
| 32 | DFSP 12 | Minor | Winston rotation task says to use winston-daily-rotate-file; Winston's own File transport already supports maxsize and maxFiles, which is enough for the "no file over 1 MB" requirement. | Reasoned | Accept either; the solution shows the built-in option. | Winston built-in maxsize/maxFiles accepted as well as winston-daily-rotate-file. |
| 33 | Both 8 | Minor | Prerequisite chain: Lab 8 requires Docker, but Docker is taught in Lab 13. The manual installs it in Lab 8 "minimally" and again in Lab 13. | Reasoned | Install Docker once in Lab 1 setup. | Docker is installed once, in Lab 1 Step 7; later labs only confirm it. |
| 34 | Both | Minor | No lab practises Git collaboration (branch, pull request, review) although CLO 3 requires it; Git first appears in Lab 15. | Reasoned | Add a Git task in Labs 3, 7, 11 and 15. | Git tasks added in Labs 1, 3, 7, 11 and 15. |
| 35 | Both 15-16 | Minor | The lecture notes use GitHub Actions and Trivy; the manual uses Jenkins. Both are free, but students need one route that matches the exam and Assignment 3. | Reasoned | Make GitHub Actions the primary and Jenkins an optional extension (or the reverse, but state it). | Both CI routes are in Lab 15 and the choice is stated: Route A Jenkins, then Route B GitHub Actions (needed for Assignment 3). |

### Added

- Lab 1 Step 7 (Git and Docker once) and Step 8 (.gitignore and first commit).
- Lab 2: exception primer; CCSP resources.csv generator.
- Lab 6: local test page for offline testing; Lab 9: local mock API.
- Lab 12: tamper-evidence step; Lab 13: build-cache, .dockerignore and --env-file demonstrations.
- Lab 15: Trivy scan and GitHub Actions route; Lab 16: complete connected pipelines for both courses.
- Evidence rules, Windows/WSL2 guidance and the lab-to-week mapping in How to Use This Manual.

### Changed: tools and versions (October 2026 check)

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

### Lab-by-lab status in the original manual (before the fixes)

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

### Known issues and open items in the revised edition

- Code in Labs 1–7 and 9–12 comes from the tested solution pack, and the new snippets (mock API, resources generator, Lab 8 harness and handlers, CCSP alert, parsers, both capstone pipelines against a local SMTP sink) were run when this edition was built. Not run: faasd (Lab 8 Tier 2), Docker (Labs 13, 14, 16 container steps), Jenkins and GitHub Actions (Lab 15), Moto/aws CLI steps and the public websites; please run Labs 13 and 15 once on a lab PC before term.
- Decision needed: whether the faasd CE EULA covers classroom use. Until then Tier 1 of Lab 8 is the graded route.
- Placeholders to fill before term: the Trivy version in the Jenkinsfile and the pinned Trivy action tag in ci.yml; check the current major versions of the GitHub actions used.
- Open: CCSP Lab 10 does not yet read costs from the Moto emulator; CCSP Labs 3, 6 and 7 still share code with Part I.
- Re-check the Moto cloud-state path (/moto-api/data.json) on the version you install.

### Limits of the verification

- The sandbox had no Docker daemon, no internet and no Jenkins, so Labs 8 (faasd), 13, 14, 15 and the Docker parts of 16 were **reasoned from documentation** , not run. The bind-mount behaviour and the missing Docker CLI in the Jenkins image are standard, well-documented behaviours, but please run Labs 13 and 15 once on a lab PC before term.
- Public sites (jsonplaceholder, books.toscrape.com) and packages (axios, nodemailer, winston, lnav) were not reachable, so those labs were tested against a local mock server or by reading the code.
- Version and licence statements for faasd, MinIO and Jenkins come from current project pages found during this review. Re-check them just before term because they can change again.


## Where to read more

- Full report: [docs/verification-report.md](docs/verification-report.md)
- Manual's own change log: [docs/manual-change-log.md](docs/manual-change-log.md)
- Lecture-week mapping: [docs/lab-to-week-mapping.md](docs/lab-to-week-mapping.md)
