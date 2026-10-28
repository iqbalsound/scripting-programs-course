# Scripting Programs: Lab Manual, Lecture Notes and Solutions (Fall 2026)

Step-by-step labs, solution code, lecture notes and assessments for two courses at the Faculty of Engineering Sciences and Technology, Hamdard University Karachi:

- **DFSP-5208 Scripting Programs** (BS Digital Forensics and Cyber Security)
- **CCSP-5213 Scripting Program and Cloud Architecture** (BS Cloud Application Development and Operations)

Instructor: Iqbal Uddin Khan. Everything uses free and open-source tools only (Python, Bash, Node.js, Git, Docker, SQLite, Moto, GitHub Actions, Jenkins).

> This repository is a structured extraction of three documents: the *Combined Laboratory Manual* (PDF), the *Lecture Notes Weeks 1-16* (DOCX) and the *Lab Manual Verification Report* (DOCX). See [CHANGELOG.md](CHANGELOG.md) for what changed in the Fall 2026 revision and [docs/EXTRACTION_NOTES.md](docs/EXTRACTION_NOTES.md) for how the extraction was done.

## How to learn from this repo (step by step)

1. Read [docs/software-and-how-to-use.md](docs/software-and-how-to-use.md) and install the tools (Windows users: WSL2 with systemd).
2. Follow the labs **in order**, Lab 1 to Lab 16, for your course. Each lab folder has a `README.md` with objectives, theory, prerequisites, the step-by-step solution and the tasks to submit, plus a `code/` folder with the scripts.
3. Read the matching lecture week in [lecture-notes/](lecture-notes/README.md) before or after each lab.
4. Tick off the tasks in `TASKS.md` of your course, then test yourself with the [assessments](assessments/README.md).

Each lab README follows the same six-part layout: title, objectives, short theory, prerequisites, step-by-step solution, required outcomes / tasks (as a checklist).

## Labs

| Lab | Topic | Lecture week | DFSP-5208 (forensics) | CCSP-5213 (cloud) |
| --- | --- | --- | --- | --- |
| 1 | Introduction to Python Scripting | 1 | [open](dfsp-5208-forensic-scripting/lab-01-python-intro/README.md) | [open](ccsp-5213-cloud-scripting/lab-01-python-intro/README.md) |
| 2 | File Handling and Automation in Python | 2 | [open](dfsp-5208-forensic-scripting/lab-02-file-handling/README.md) | [open](ccsp-5213-cloud-scripting/lab-02-file-handling/README.md) |
| 3 | Command-Line Tools with Python (argparse) | 3 | [open](dfsp-5208-forensic-scripting/lab-03-argparse-cli/README.md) | [open](ccsp-5213-cloud-scripting/lab-03-argparse-cli/README.md) |
| 4 | Fundamentals of Bash Scripting | 4 | [open](dfsp-5208-forensic-scripting/lab-04-bash-basics/README.md) | [open](ccsp-5213-cloud-scripting/lab-04-bash-basics/README.md) |
| 5 | Automating System Tasks with Bash (cron) | 5 | [open](dfsp-5208-forensic-scripting/lab-05-cron-backups/README.md) | [open](ccsp-5213-cloud-scripting/lab-05-cron-backups/README.md) |
| 6 | Web Scraping with Python (BeautifulSoup) | 6 | [open](dfsp-5208-forensic-scripting/lab-06-web-scraping/README.md) | [open](ccsp-5213-cloud-scripting/lab-06-web-scraping/README.md) |
| 7 | Node.js Scripting for File System Automation | 7 | [open](dfsp-5208-forensic-scripting/lab-07-nodejs-filesystem/README.md) | [open](ccsp-5213-cloud-scripting/lab-07-nodejs-filesystem/README.md) |
| 8 | Deploying Node.js Scripts as Serverless Functions | 8 | [open](dfsp-5208-forensic-scripting/lab-08-serverless-functions/README.md) | [open](ccsp-5213-cloud-scripting/lab-08-serverless-functions/README.md) |
| 9 | REST API Interaction: Fetching and Parsing JSON Data | 10 | [open](dfsp-5208-forensic-scripting/lab-09-rest-api-json/README.md) | [open](ccsp-5213-cloud-scripting/lab-09-rest-api-json/README.md) |
| 10 | Automating Security Workflows with APIs | 11 | [open](dfsp-5208-forensic-scripting/lab-10-api-workflows/README.md) | [open](ccsp-5213-cloud-scripting/lab-10-api-workflows/README.md) |
| 11 | Error Handling and Debugging in Scripts | 12 | [open](dfsp-5208-forensic-scripting/lab-11-error-handling-debugging/README.md) | [open](ccsp-5213-cloud-scripting/lab-11-error-handling-debugging/README.md) |
| 12 | Logging and Monitoring in Security Scripts | 13 | [open](dfsp-5208-forensic-scripting/lab-12-logging-monitoring/README.md) | [open](ccsp-5213-cloud-scripting/lab-12-logging-monitoring/README.md) |
| 13 | Introduction to Docker: Containerizing Forensic Tools | 14 | [open](dfsp-5208-forensic-scripting/lab-13-docker/README.md) | [open](ccsp-5213-cloud-scripting/lab-13-docker/README.md) |
| 14 | Automating Container Deployment | 14 (2nd half) or 15 | [open](dfsp-5208-forensic-scripting/lab-14-container-deployment/README.md) | [open](ccsp-5213-cloud-scripting/lab-14-container-deployment/README.md) |
| 15 | CI/CD Pipeline Automation for Secure Deployment | 15 | [open](dfsp-5208-forensic-scripting/lab-15-cicd-pipeline/README.md) | [open](ccsp-5213-cloud-scripting/lab-15-cicd-pipeline/README.md) |
| 16 | Capstone Lab: Designing and Deploying a Complete Forensic Pipeline | 16 | [open](dfsp-5208-forensic-scripting/lab-16-capstone/README.md) | [open](ccsp-5213-cloud-scripting/lab-16-capstone/README.md) |

Note the week offset: Week 9 is the midterm, so Labs 9-16 are taught one lecture week later (see [docs/lab-to-week-mapping.md](docs/lab-to-week-mapping.md)).

## Repository layout

```text
.
├── README.md
├── CHANGELOG.md                      # findings and changes, from the verification report
├── docs/
│   ├── software-and-how-to-use.md    # tool list, WSL2 setup, evidence rules
│   ├── lab-to-week-mapping.md
│   ├── manual-change-log.md          # change log printed in the manual
│   ├── verification-report.md        # full verification report
│   └── EXTRACTION_NOTES.md
├── dfsp-5208-forensic-scripting/     # Part I
│   ├── README.md   TASKS.md
│   └── lab-01-python-intro/ ... lab-16-capstone/   (README.md + code/)
├── ccsp-5213-cloud-scripting/        # Part II (same layout)
├── lecture-notes/
│   ├── 00-course-overview/
│   └── week-01-... to week-16-...    (README.md + code/)
└── assessments/                      # quizzes, assignments, class task, exam blueprint, appendices
```

## Known limits (please read)

- Labs 13, 14, 15 and the Docker parts of Lab 16 were reasoned from documentation, not run, by the original verification. Lab 8 Tier 2 (faasd) was not run either. Run them once before relying on them.
- The faasd CE licence (non-commercial, personal use) needs a decision for classroom use; the local harness (Lab 8 Tier 1) is the graded path.
- Public sites used in labs (jsonplaceholder, books.toscrape.com) may be unavailable; the labs include local mock fallbacks.
- Some steps contain placeholders you must fill in (for example the Trivy version in the Jenkinsfile and the action tag in `ci.yml`).
- Replace `YOUR-ROLL-NUMBER` and similar personal values with your own.

## Licence

No licence file is included. Add one before publishing (for example CC BY-NC-SA 4.0 for course material, MIT for the code) after checking what your university allows.
