# Week 4: Bash Scripting Fundamentals

[⬅ Lecture notes index](../README.md)

| Mapped CLO | Suggested readings | Lab / activity |
| --- | --- | --- |
| CLO 1 (Apply) | Garrels, Bash Guide for Beginners, Ch. 1-3 | Directory operations and cleanup script |


### Learning objectives

- Write Bash scripts with variables, conditionals, loops and arguments.
- Combine tools with pipes (`grep`, `awk`, `sort`, `uniq`, `cut`).
- Schedule a task with cron.


### Hour 1: Bash basics

- Shebang, `chmod +x`, variables, quoting (`"$var"` always), `$1`, `$#`.
- Conditionals: `if [ -f "$file" ]`, `[[ ... ]]`; loops: `for f in *.log`.
- Always quote variables and test on a copy of the data.

> Forensic track (DFSP-5208, BS Digital Forensics & Cyber Security) Directory layout for evidence: case/YYYYMMDD/{raw,working,reports}. Script it.

> Cloud track (CCSP-5213, BS Cloud Application Development & Operations) Organize a folder of exported cloud logs by date and region.


### Hour 2: Pipes and system-level automation

- `grep "Failed" auth.log | awk '{print $11}' | sort | uniq -c | sort -nr | head`
- Redirection: `>`, `>>`, `2>&1`.
- cron: the five fields, `crontab -e`, logging cron output to a file. Windows students use WSL cron or Task Scheduler.


### Hour 3: Lab

- Write `cleanup.sh`: take a directory and an age in days, list files older than that, ask for confirmation, then delete. Default to a dry run.
- Schedule the dry run every hour and verify it fires once.

```bash
#!/usr/bin/env bash
dir="$1"; days="${2:-7}"
[ -d "$dir" ] || { echo "Not a directory: $dir" >&2; exit 1; }
find "$dir" -type f -mtime +"$days" -print
```

> 📁 Saved as [`code/cleanup.sh`](code/cleanup.sh)


### In-class / take-home questions (evidence-based)

> Evidence rule Every answer must be backed by output produced on the student's own machine this week (terminal output, screenshot showing the system clock, file hash or log). Generic, non-executed answers earn zero. Parameters are personalized, see the Appendix on personalization.

1. Paste the output of your dry-run on your own test folder, showing the file list.
1. Run with a non-existent directory and paste the message and the exit code (`echo $?`).
1. Show your crontab line (or Task Scheduler screenshot) with the schedule expression, and the first log line proving it fired. Include the system clock.
1. Write a one-line pipe that reports the three most frequent values in a column of a file you created. Paste the command and its output.
1. Explain, using one real command from your script, why quoting `"$dir"` matters when a folder name contains a space. Demonstrate it.

## Code files in this week

- [`code/cleanup.sh`](code/cleanup.sh)
