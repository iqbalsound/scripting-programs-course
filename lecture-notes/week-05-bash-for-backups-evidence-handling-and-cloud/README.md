# Week 5: Bash for Backups, Evidence Handling and Cloud CLI

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 1 (Apply) | Garrels, Bash Guide for Beginners, Ch. 5-6 | Backup with cron and hashing |

> Revised for Fall 2026 Cloud CLI without a cloud account: use the AWS CLI with --endpoint-url http://localhost:5000 pointing to Moto (or another emulator). No real account or card is needed. New: Bash safety (set -euo pipefail, trap) is the Bash equivalent of the exception primer.


### Learning objectives

- Write Bash functions and handle errors with exit codes and `trap`.
- Automate backup with integrity verification.
- Use a cloud CLI against a local endpoint.


### Hour 1: Advanced Bash

- Functions, `return`, `local`.
- `set -euo pipefail` and why it fails fast; `trap cleanup EXIT`.
- Logging from Bash with timestamps: `echo "$(``date -u +%FT%TZ) message" >> run.log`.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Case study: evidence backup that copies, then verifies with sha256sum -c.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Case study: VM snapshot automation that must not run twice at once (lock file).


### Hour 2: Integration with cloud CLI

- AWS CLI / Azure CLI install and `--endpoint-url`.
- Forensics: upload or sync a verified backup to object storage and record the hash.
- Never put access keys in scripts; use environment variables or a credentials profile.

```text
aws --endpoint-url http://localhost:5000 s3 mb s3://lab-evidence
aws --endpoint-url http://localhost:5000 s3 cp backup.tar.gz s3://lab-evidence/
```


### Hour 3: Lab

- Build `backup.sh`: tar a folder, write `SHA256SUMS`, verify, copy to a destination and log each step.
- Schedule it with cron every six hours (or every 5 minutes for the demonstration).


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalised, see the Appendix on personalisation.

1. Paste your full `backup.sh` and one complete run log with timestamps.
1. Corrupt the backup file by one byte and run verification. Paste the failure output and exit code.
1. Show your crontab entry and the log lines from two consecutive scheduled runs.
1. Show a `trap` or error branch in your script and the exact line it printed when you caused a failure on purpose.
1. List the object(s) in your storage bucket (CLI output with the endpoint URL) and the SHA-256 recorded for the uploaded file.
