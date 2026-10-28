# Course overview, revision summary and lab environment

[⬅ Lecture notes index](../README.md)

# 1. Fall 2026 Revision Summary

This document merges the two course tracks into one teaching pack: **DFSP-5208 Scripting Programs** (BS Digital Forensics and Cyber Security) and **CCSP-5213 Scripting Program and Cloud Architecture** (BS Cloud Application Development and Operations). Both are 2+1 credit hour, Semester 6 courses with the same instructor, the same 16-week structure and the same three CLOs. Where the two tracks differ, the text carries a blue **Forensic** box or a green **Cloud** box. Everything else is shared, so you can teach both sections from one set of slides.

I re-analyses all five files (Weeks 1-8 combined notes, Weeks 9-15 notes for each course, and both approved course outlines) against each other and against the tooling that is current as of October 2026. The table below lists what I found and what I changed. The most urgent item is the first one.

| # | Finding | Where it appeared | Change made in this document |
| --- | --- | --- | --- |
| 1 | LocalStack Community Edition no longer exists as a free anonymous image. Since 23 March 2026, localstack/localstack requires an account and auth token; the free tier is non-commercial only and the Community image is frozen. | CCSP Weeks 10, 11, 15 | Primary emulator is now Moto (pip install "moto[server]", no Docker, no account). LocalStack (free Hobby token) and Floci (MIT, no token) are listed as options. Please do a dry run of your chosen emulator before Week 10. |
| 2 | Week 8 serverless lab assumes a real AWS Lambda / Azure Functions account (card and billing risk for students). | Both outlines, Week 8 | Four-tier lab: local Node harness, emulator Lambda, Azure Functions Core Tools, and optional real cloud for students who already have an account. |
| 3 | Suggested reading mismatches: Week 10 cites *Practical Malware Analysis* Ch. 6 (x86 control flow, not REST). Week 13 cites *Docker Deep Dive* Ch. 2-3 for logging. Week 11 cites *Automate the Boring Stuff* Ch. 14, which is Google Sheets in the 2nd edition. | Outlines and notes | Replacement readings suggested (Python docs, Real Python style references, ATBS 2nd ed. Ch. 16-18). Please verify chapter numbers against your edition. |
| 4 | The one-hour mid-semester test requires try/except and logging, but those are first taught in Weeks 12-13, after the test. | Both notes, class task | Short primers added: exceptions in Week 2, logging basics in Week 3, Bash exit codes in Week 5. Full treatment stays in Weeks 12-13. |
| 5 | CLO 3 requires version control, but no week teaches Git. | Both outlines | A Git thread now runs through Weeks 1, 3, 7, 12 and 15 (init, commit, branch, pull request, review). |
| 6 | Assignment 2 is a Node.js API task, but Week 10 teaches only Python requests. | Notes Weeks 10, Assignment 2 | Node.js fetch/axios parity added to Week 10. |
| 7 | datetime.utcnow() is deprecated from Python 3.12 (the version used in the Docker lab). | Weeks 10, Week 13 | Replaced with timezone-aware datetime.now(timezone.utc). |
| 8 | Week 14 .dockerignore excludes .env, but the workflow script needs the API key at run time; image also runs as root. | Week 14 | Added --env-file, non-root USER, pinned base tag, and a "secrets never baked into images" check. |
| 9 | Commands are Linux/macOS only (source venv/bin/activate, $(pwd), sha256sum, cron). Most lab PCs run Windows. | Weeks 10-15 | Command equivalents table in Section 3 and inline Windows notes. |
| 10 | CI workflow uses trivy-action@master and unpinned actions, and the Trivy step never fails the build. This is a supply-chain risk in a security course. | Week 15 | Pin actions to tagged releases or commit SHAs, set least-privilege permissions, make Trivy fail on HIGH/CRITICAL. |
| 11 | Email alerting depends on a personal mail provider; smtpd was removed in Python 3.12. | Week 11 | Webhook alert is primary; aiosmtpd local debug SMTP server added for offline email demos. |
| 12 | Week 13 log-hash exercise: a live log changes every time it is written, so start/end hashes always differ. The basicConfig + RotatingFileHandler snippets also conflict. | Week 13 | Corrected configuration and a better tamper-evidence exercise (hash a closed/rotated file, store the hash separately). |
| 13 | Week 16 has no lecture notes although both outlines schedule it. | Both | Week 16 added (best practices, final project presentations, rubric). |
| 14 | Quiz 3 says "Weeks 11-16" but draws on "Weeks 10-15"; Assignment 3 rubric omits Git; the class-task CLO mapping differs between sections of the DFSP outline (marks 3/4/3, indicative 30/40/30, but Assessment Methods lists only CLO 2 and 3). The CCSP indicative table says 20/50/30. | Outlines | Assessment pack aligned to the marks distribution tables (the approved totals: CLO 1 = 25, CLO 2 = 41, CLO 3 = 34). Please correct the indicative percentage rows at the next outline revision. |
| 15 | Weeks 1-8 notes are bullet-level and the scenario questions can be answered by a chatbot in one paste. | Weeks 1-8 notes | Each week expanded with teaching points, a lab, and evidence-based, personalised questions. See Appendix C. |
| 16 | Free-tier APIs change. A key-based lab can fail on the day. | Week 10 | Added a 25-line instructor mock API (with a deliberate 429 after three calls) as a guaranteed fallback. |
| 17 | Promtail is deprecated in favour of Grafana Alloy; the Cloud Week 13 step points Promtail at a log file. | CCSP Week 13 | Use Grafana Alloy, or push lines to the Loki HTTP API as a simple fallback. |

> Items I could not verify and you should check before term 1. Current free-tier limits and the exact endpoint/header format of AbuseIPDB (or any alternative API you choose). 2. Chapter numbers in your edition of each textbook. 3. Whether your lab PCs permit Docker (virtualisation / WSL 2) and outbound access to Docker Hub, PyPI, npm and GitHub. 4. Current major versions of actions/checkout, actions/setup-python and aquasecurity/trivy-action. 5. Moto's /moto-api/ status endpoint behaviour on the version you install. Fall 2026 calendar dates were not in the files, so the pack uses week numbers only.

# 2. Course Overview and Assessment Map


### Course learning outcomes

| CLO | BT level | DFSP-5208 (Forensics) | CCSP-5213 (Cloud) |
| --- | --- | --- | --- |
| CLO 1 | Apply (L3) | Apply Python, Bash, JavaScript to automate forensic and cybersecurity tasks. | Apply Python, Bash, JavaScript to automate tasks and interact with cloud services. |
| CLO 2 | Create (L6) | Design and deploy security-focused applications using APIs, automation and containerization. | Design and deploy cloud-native applications using containerization, serverless computing and APIs. |
| CLO 3 | Analyze (L4) | Demonstrate debugging, error handling and collaborative project management using version control in forensic scripting projects. | Demonstrate debugging, error handling and collaborative project management using version control in cloud-based scripting projects. |


### Marks distribution (identical in both courses)

| Assessment | Weeks | Marks | CLO 1 | CLO 2 | CLO 3 |
| --- | --- | --- | --- | --- | --- |
| Assignment 1 | 1-5 | 3 | 3 | 0 | 0 |
| Assignment 2 | 6-10 | 3 | 0 | 2 | 1 |
| Assignment 3 | 11-16 | 4 | 0 | 2 | 2 |
| Quiz 1 | 1-5 | 3 | 2 | 1 | 0 |
| Quiz 2 | 6-10 | 3 | 0 | 2 | 1 |
| Quiz 3 | 11-16 | 4 | 0 | 2 | 2 |
| One-hour class task | Mid-semester | 10 | 3 | 4 | 3 |
| Midterm exam | 1-8 | 20 | 12 | 8 | 0 |
| Final exam | 1-16 | 50 | 5 | 20 | 25 |
| Total |  | 100 | 25 | 41 | 34 |


### Sixteen-week teaching map

| Wk | Topic | Lab | CLO | Assessment event |
| --- | --- | --- | --- | --- |
| 1 | Scripting vs programming; role in security and cloud | Hello script, environment, Git init | 1 | Quiz 1 window opens |
| 2 | Python basics, functions, files, exception primer | Parse log / CSV | 1 |  |
| 3 | Python automation, JSON/CSV, argparse CLI, logging primer | CLI log or CSV tool | 1 | Assignment 1 issued |
| 4 | Bash fundamentals, pipes, cron intro | Directory + cleanup script | 1 |  |
| 5 | Bash for backups and CLI integration, exit codes | Backup with cron + hashing | 1 | Quiz 1; Assignment 1 due |
| 6 | Web scraping and data feeds | Scrape to CSV | 1 | Assignment 2 issued |
| 7 | Node.js basics | File-renaming script | 1 |  |
| 8 | Node.js serverless deployment | Local-first serverless lab | 2 | One-hour class task (suggested) |
| 9 | Midterm examination | None | 1, 2 | Midterm (Weeks 1-8) |
| 10 | REST APIs and JSON | Fetch, save, hash | 1 | Quiz 2; Assignment 2 due |
| 11 | Automating workflows with APIs | Fetch-evaluate-alert, SQLite, scheduler | 2 | Assignment 3 issued |
| 12 | Error handling, debugging, Git collaboration | pdb, custom exceptions, PRs | 3 |  |
| 13 | Logging and monitoring | Logging, Winston, optional Loki | 3 |  |
| 14 | Docker and containerisation | Build and run image | 2 |  |
| 15 | CI/CD with GitHub Actions | Test, build, scan pipeline | 2 | Quiz 3 |
| 16 | Best practices; final presentations | Capstone demos | 2, 3 | Assignment 3 due; final exam revision |

# 3. Lab Environment and Command Equivalents

Install and test the following **before Week 1** on a sample lab PC and on your own laptop. All tools are free or have a free personal/education tier.

- **Python 3.12 or newer** , VS Code, Git. Packages: `requests`, `python-dotenv`, `beautifulsoup4`, `boto3` (Cloud track), `moto[server]` (Cloud track), `aiosmtpd` (optional).
- **Node.js current LTS** (22 or 24) with npm. Node 18+ has built-in `fetch`; `axios` and `winston` are installed with npm.
- **Bash** : native on Linux/macOS; on Windows use WSL 2 (Ubuntu) or Git Bash. Weeks 4-5 assume a Linux shell.
- **Docker Engine** (Linux) or **Docker Desktop** (free for education and personal use; check the current terms for the university lab). WSL 2 backend on Windows.
- A free **GitHub** account per student (needed from Week 3). Use a shared GitHub Classroom or organisation if the department has one.

| Task | Linux / macOS / WSL | Windows (PowerShell) |
| --- | --- | --- |
| Create venv | python3 -m venv venv | python -m venv venv |
| Activate venv | source venv/bin/activate | venv\Scripts\Activate.ps1 |
| SHA-256 of a file | sha256sum file | Get-FileHash file -Algorithm SHA256 |
| Current dir in docker -v | -v "$(pwd)/evidence:/app/evidence" | -v "${PWD}/evidence:/app/evidence" |
| Schedule every 30 min | crontab -e then */30 * * * * ... | Task Scheduler, or schtasks /create /sc minute /mo 30 /tn Job /tr "python C:\path\workflow.py" |
| Environment variable (session) | export API_KEY=... | $env:API_KEY = "..." |
| Show system clock in screenshot | date -u; date | Get-Date; (Get-Date).ToUniversalTime() |
| Find text in files | grep -rn "ERROR" . | Select-String -Path *.log -Pattern ERROR |
