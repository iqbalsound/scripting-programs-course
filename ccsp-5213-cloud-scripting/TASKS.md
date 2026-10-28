# CCSP-5213: all lab tasks (Required Outcomes)

Tick these off as you go. Each task links back to the lab it comes from.


## Lab 1: Introduction to Python Scripting: Writing and Executing Basic Scripts

[Open lab](lab-01-python-intro/README.md)

- [ ] Screenshot of `python3 --version` showing 3.12 or newer, with the system clock visible.
- [ ] Submit hello_cloud.py (with your own roll number filled in) together with a terminal screenshot of its output, system clock visible.
- [ ] One-paragraph written reflection: how does an interpreted script differ from a compiled C/Java program?
- [ ] Screenshot of `git status` showing that the virtual environment (.venv) folder is excluded by .gitignore (used from Lab 3 onward).
- [ ] Screenshot of `docker run --rm hello-world` succeeding (or a note from your instructor that Docker is not available on your lab PC).


## Lab 2: File Handling and Automation in Python

[Open lab](lab-02-file-handling/README.md)

- [ ] sample_data.csv, errors_only.csv, and run_history.log submitted together, with a screenshot of the run (system clock visible).
- [ ] resources.csv generated with generate_resources.py (30 rows; id, region, status).
Extend filter_errors.py so it also writes warn_only.csv and prints the percentage of rows at each level; submit the modified script.
- [ ] Explain in 2–3 sentences why `with open(...)` is preferred over calling open()/close() manually.


## Lab 3: Command-Line Tools with Python (argparse)

[Open lab](lab-03-argparse-cli/README.md)

- [ ] log_filter_cli.py submitted with a screenshot of the --help output (system clock visible).
- [ ] Output CSV files for both ERROR and WARN levels, and the printed count matching `wc -l` minus one.
- [ ] README.md documenting --limit, plus one additional optional flag of your own choice (e.g. --host NAME).
- [ ] Screenshot of `git log --oneline` showing at least one commit for this lab.


## Lab 4: Fundamentals of Bash Scripting

[Open lab](lab-04-bash-basics/README.md)

- [ ] organize.sh submitted along with a terminal screenshot of a successful run (system clock visible), showing the per-category counts.
- [ ] Extend the script with a fourth category (for example *.json into a json/ folder) and update the summary line; submit the modified script.
- [ ] Short written answer: what happens if `set -euo pipefail` is removed and the script hits an error midway? Give one example for each flag.


## Lab 5: Automating System Tasks with Bash (cron)

[Open lab](lab-05-cron-backups/README.md)

- [ ] backup.sh submitted with the crontab entry shown in a screenshot (system clock visible).
- [ ] backup_history.log showing at least two automatic (unattended) runs about 10 minutes apart.
- [ ] Screenshot of `sha256sum -c SHA256SUMS` reporting OK, and of `grep -c venv` printing 0.
- [ ] Explain why the redirection `>> cron.out 2>&1` is needed in the crontab line, and what the retention line (find `... -mtime +7` -delete) does.
- [ ] Screenshot of the `aws s3 ls` listing showing the backup archive in the lab-backups bucket.


## Lab 6: Web Scraping with Python (BeautifulSoup)

[Open lab](lab-06-web-scraping/README.md)

- [ ] scraper.py and scraped_books.csv submitted, with a screenshot of the run (system clock visible).
- [ ] Screenshot of the offline test (one record saved, one malformed item skipped) and of the failure case with its exit code.
- [ ] Extend the scraper to follow the “next” page link for up to 3 pages, with a 1-second pause between page requests.
- [ ] One paragraph explaining what robots.txt is and why rate limiting matters ethically and legally.


## Lab 7: Node.js Scripting for File System Automation

[Open lab](lab-07-nodejs-filesystem/README.md)

- [ ] rename_cloud_files.js submitted with before/after directory listing screenshots (system clock visible), including the dry run.
- [ ] Extend the script with a `--prefix NAME` option that replaces the timestamp text in the new file name, on a feature branch, and submit the pull-request link or a screenshot of the reviewed pull request.
- [ ] Short comparison table (3 rows) contrasting Python's pathlib/os calls with Node's `fs/promises` equivalents.


## Lab 8: Deploying Node.js Scripts as Serverless Functions

[Open lab](lab-08-serverless-functions/README.md)

- [ ] Harness output for an over-budget and an under-budget resource, system clock visible.
- [ ] Change THRESHOLD_USD to an instructor-provided value and resubmit handler.js with new test output.
- [ ] Output showing that a non-JSON body is rejected with status 400 instead of crashing the function.
- [ ] Optional (Tier 2): screenshot of `faas-cli list` showing the deployed usage-alert function and the curl output.


## Lab 9: REST API Interaction: Fetching and Parsing JSON Data

[Open lab](lab-09-rest-api-json/README.md)

- [ ] One evidence_*.json file, custody.log showing its matching SHA-256, and resources.db submitted, with a screenshot of the sqlite3 query (system clock visible).
- [ ] fetch_resources.js console.table output screenshot.
- [ ] Screenshots showing both scripts handling a non-200 status or a network failure without crashing, and exiting with a non-zero code.
- [ ] Evidence file and custody-log line created from the Moto emulator's cloud-state JSON.
- [ ] Add API-key loading from .env and 429 handling (Step 9) to the Python script, and document the behaviour in two sentences.


## Lab 10: Automating Workflows with APIs

[Open lab](lab-10-api-workflows/README.md)

- [ ] Screenshot of the mail sink (Mailpit web UI or aiosmtpd terminal) showing one consolidated alert email, system clock visible.
- [ ] Both alert_workflow.py and alert_workflow.js submitted.
- [ ] Extend either script with your own list of 5 resources and a budget equal to the last two digits of your roll number; show the consolidated email.
- [ ] Output of `SELECT * FROM alerts;` after the state extension, and a second run that sends no email.


## Lab 11: Error Handling and Debugging in Scripts

[Open lab](lab-11-error-handling-debugging/README.md)

- [ ] messy_billing.csv (with at least 3 deliberately malformed rows) and the corrected script submitted.
- [ ] parse_errors.log showing timestamped lines for the malformed rows being caught, not crashing the program.
- [ ] Screenshot of the VS Code debugger paused at a breakpoint with the Variables panel visible, or a pdb transcript showing `p` row, with the system clock visible.
- [ ] Screenshot of the RetryExhausted demonstration, and the link to your reviewed pull request.
- [ ] Two sentences: why is `except (KeyError, ValueError)` better than a bare except?


## Lab 12: Logging and Monitoring in Cloud-Based Scripts

[Open lab](lab-12-logging-monitoring/README.md)

- [ ] pipeline.log, pipeline.jsonl and pipeline.json.log submitted, with at least one message at each of the INFO, WARNING and ERROR levels.
- [ ] Screenshot of lnav showing a filtered view (only WARNING/ERROR lines), with the system clock visible.
- [ ] A rotated file (pipeline.log.1), its hash recorded in log_hashes.txt, and a screenshot of `sha256sum -c log_hashes.txt` showing OK, then FAILED after you change one character.
- [ ] Configure winston so that no single file exceeds 1 MB (maxsize and maxFiles, or winston-daily-rotate-file) and show the setting.
- [ ] Add the fields resource and region to the JSON context of every message.


## Lab 13: Introduction to Docker: Containerizing Applications

[Open lab](lab-13-docker/README.md)

- [ ] Dockerfile and .dockerignore submitted along with `docker images` output showing the built image (system clock visible).
- [ ] out/output.csv produced by the containerized run, with `sha256sum` showing that it matches the host-run output from Lab 3.
- [ ] Screenshot of the second build showing CACHED layers, and of the --env-file demonstration.
- [ ] One paragraph: what would need to change in the Dockerfile to add a healthcheck for this container, and does a run-once batch job need one?


## Lab 14: Automating Container Deployment

[Open lab](lab-14-container-deployment/README.md)

- [ ] Output of `curl http://localhost:5000/v2/_catalog` showing the pushed image (system clock visible).
- [ ] The list_objects_v2 output showing output.csv in the pipeline-artifacts bucket, and `identical` from the cmp command.
- [ ] Screenshot of the pull-then-run sequence proving the image was retrieved fresh from the registry.
- [ ] Short note comparing a self-hosted S3 emulator with a managed cloud storage free tier (durability, scaling, IAM, limits, account and billing).


## Lab 15: CI/CD Pipeline Automation

[Open lab](lab-15-cicd-pipeline/README.md)

- [ ] Jenkinsfile submitted alongside a screenshot of a green pipeline run showing the Build, Test, Scan and Push stages, with the system clock visible.
- [ ] Console output log from the Test stage showing the containerised script executed correctly.
- [ ] Confirm via `curl http://localhost:5000/v2/cloud-log-filter/tags/list` that the new build tag was pushed.
- [ ] Route B: ci.yml submitted with a screenshot of a green GitHub Actions run, and a screenshot of the branch-protection rule.
- [ ] Short answer: why does Test come before Build/Push, and what does `exit-code: 1` do in the scan stage?


## Lab 16: Capstone Lab: Designing and Deploying a Complete Cloud-Native Application

[Open lab](lab-16-capstone/README.md)

- [ ] Complete capstone repository (scripts/, faas/, docker/, jenkins/, run_pipeline.sh, and the design diagram).
- [ ] A successful end-to-end run log (or screen recording, system clock visible) from ingestion through to the archived output, its verified SHA-256, and the alert email.
- [ ] 5–10 minute live or recorded demo presented to the instructor, with a short Q&A on design trade-offs.
- [ ] One-page written reflection: which lab's tool was hardest to integrate, and how was the problem resolved?
