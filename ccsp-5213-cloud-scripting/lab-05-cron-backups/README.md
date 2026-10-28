# Lab 5: Automating System Tasks with Bash (cron)

**Course:** CCSP-5213  |  **Lecture week:** 5  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Schedule a Bash script to run automatically using cron (free, built into Linux).
- Automate a timestamped backup of cloud working files.
- Read and interpret crontab syntax and system logs for scheduled jobs.

## Short theory

Manually running backup or cleanup scripts is unreliable; cron a scheduler bundled with every Linux distribution at no cost, runs scripts unattended at fixed intervals. This is the same mechanism production servers use to run nightly backups, log rotation, and health checks. This lab builds a backup script and schedules it, mirroring how a cloud operations team would automate evidence/data preservation.
Every command also ends with an exit code: 0 means success and anything else means failure. Cron cannot show a terminal, so a scheduled script must report problems through its exit code and a log file. The backup script below checks its own archive and records a SHA-256 hash, so an altered or damaged backup is detected.

## Prerequisites

- Lab 4 completed.
- Access to a Linux shell with cron installed and systemd running (sudo `apt install cron` on Ubuntu if missing). On WSL, enable systemd as described in How to Use This Manual.

## Step-by-step solution


### Step 1: Confirm cron is installed and running


```bash
sudo apt install -y cron
sudo systemctl enable --now cron
sudo systemctl status cron --no-pager
```


### Step 2: Write the backup script

Create the lab folder and write backup.sh. The corrected script excludes .venv and node_modules (otherwise every run archives hundreds of megabytes), writes a SHA-256 checksum, verifies that the archive can be read, and deletes backups older than 7 days.

```bash
mkdir -p ~/cloud-scripting/lab05 && cd ~/cloud-scripting/lab05
```


```bash
#!/usr/bin/env bash
# backup.sh: timestamped, verified backup with 7-day retention. Paths can be overridden for testing.
set -euo pipefail
SRC_DIR="${SRC_DIR:-$HOME/cloud-scripting}"
BACKUP_ROOT="${BACKUP_ROOT:-$HOME/cloud-backups}"
TS=$(date -u +%Y%m%d_%H%M%S)
ARCHIVE="${BACKUP_ROOT}/backup_${TS}.tar.gz"
mkdir -p "$BACKUP_ROOT"

tar --exclude='.venv' --exclude='node_modules' -czf "$ARCHIVE" -C "$SRC_DIR" .
( cd "$BACKUP_ROOT" && sha256sum "$(basename "$ARCHIVE")" >> SHA256SUMS )
tar -tzf "$ARCHIVE" > /dev/null                       # verify the archive can be read
echo "$(date -u +%FT%TZ) backup_${TS}.tar.gz created and verified" >> "$BACKUP_ROOT/backup_history.log"

find "$BACKUP_ROOT" -name 'backup_*.tar.gz' -mtime +7 -delete   # retention: 7 days
```

> 📁 Saved as [`code/backup.sh`](code/backup.sh)


### Step 3: Make it executable and test manually


```bash
chmod +x ~/cloud-scripting/lab05/backup.sh
mkdir -p ~/cloud-scripting/.venv && echo test > ~/cloud-scripting/.venv/junk   # a file that must NOT be backed up
~/cloud-scripting/lab05/backup.sh
echo "exit code: $?"
ls ~/cloud-backups
cd ~/cloud-backups && sha256sum -c SHA256SUMS
tar -tzf backup_*.tar.gz | grep -c venv   # expect 0
```

A second test shows a failure being reported: run SRC_DIR=/nonexistent ~/cloud-scripting/lab05/backup.sh; echo $? and confirm that the exit code is not 0.

### Step 4: Schedule it with cron

Edit the crontab to run the backup every 10 minutes for demonstration purposes (a real deployment would use a nightly schedule). The output redirection matters: cron has no terminal, so any error message would otherwise be lost.

```bash
crontab -e
# add these lines, then save:
# demonstration: every 10 minutes
*/10 * * * * $HOME/cloud-scripting/lab05/backup.sh >> $HOME/cloud-backups/cron.out 2>&1
# real use: nightly at 02:00
# 0 2 * * * $HOME/cloud-scripting/lab05/backup.sh >> $HOME/cloud-backups/cron.out 2>&1
```


### Step 5: Verify scheduled execution


```bash
crontab -l
# wait 20+ minutes, then:
cat ~/cloud-backups/backup_history.log
```

On WSL without systemd, run sudo service cron start after each restart; Windows students without WSL may use Task Scheduler (schtasks).

### Step 6: Copy the backup to S3-compatible storage with the cloud CLI

The course outline lists a cloud CLI. Use the free Moto S3 emulator so no cloud account is needed. The dummy credentials test/test are accepted by the emulator.

```bash
source ~/cloud-scripting/lab01/.venv/bin/activate
pip install "moto[server]" awscli
moto_server -p 5000 &
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=us-east-1
aws --endpoint-url http://localhost:5000 s3 mb s3://lab-backups
LATEST=$(ls -t ~/cloud-backups/backup_*.tar.gz | head -1)
aws --endpoint-url http://localhost:5000 s3 cp "$LATEST" s3://lab-backups/
aws --endpoint-url http://localhost:5000 s3 ls s3://lab-backups/
```


## Required outcomes / tasks

- [ ] backup.sh submitted with the crontab entry shown in a screenshot (system clock visible).
- [ ] backup_history.log showing at least two automatic (unattended) runs about 10 minutes apart.
- [ ] Screenshot of `sha256sum -c SHA256SUMS` reporting OK, and of `grep -c venv` printing 0.
- [ ] Explain why the redirection `>> cron.out 2>&1` is needed in the crontab line, and what the retention line (find `... -mtime +7` -delete) does.
- [ ] Screenshot of the `aws s3 ls` listing showing the backup archive in the lab-backups bucket.

## Code files in this lab

- [`code/backup.sh`](code/backup.sh)
