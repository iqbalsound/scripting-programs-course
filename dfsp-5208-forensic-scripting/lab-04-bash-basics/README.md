# Lab 4: Fundamentals of Bash Scripting

**Course:** DFSP-5208  |  **Lecture week:** 4  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Write and run Bash scripts on Linux (native, WSL2, or macOS Terminal, all free).
- Use variables, conditionals, and loops to automate directory operations.
- Understand exit codes and basic error handling in shell scripts.

## Short theory

Bash (Bourne Again SHell) ships free with every Linux distribution and macOS, and is available on Windows through WSL2 (Windows Subsystem for Linux, free and open source). Much of forensic tooling is glued together with shell scripts because Bash has direct, low-overhead access to the file-system and system utilities. This lab covers the syntax needed for the automation labs that follow.

## Prerequisites

- A Bash shell: native on Linux/macOS, or WSL2 (wsl --install) on Windows 11.
- Basic familiarity with terminal navigation (cd, ls, mkdir).

## Step-by-step solution


### Step 1: Verify Bash version


```bash
bash --version   # GNU bash, version 5.x expected
```


### Step 2: Create the lab folder


```bash
mkdir -p ~/forensic-scripting/lab04 && cd ~/forensic-scripting/lab04
```


### Step 3: Write a directory-organiser script

Create organize.sh that creates dated sub-folders and moves files into them based on extension. The corrected script skips itself, counts items per category, handles names with spaces, and never overwrites an existing file (it prefixes the time instead, so both copies of evidence are kept).

```bash
#!/usr/bin/env bash
# organize.sh: move files in a folder into dated archive sub-folders by extension.
# set -e: exit on any error; set -u: error on unset variables; set -o pipefail: a pipeline fails if any stage fails.
set -euo pipefail

TARGET_DIR="${1:-.}"
[ -d "$TARGET_DIR" ] || { echo "Not a directory: $TARGET_DIR" >&2;
exit 1; }
DATE_TAG=$(date +%Y-%m-%d)
ARCHIVE="${TARGET_DIR}/archive_${DATE_TAG}"
SELF="$(basename "${BASH_SOURCE[0]}")"

mkdir -p "${ARCHIVE}/logs" "${ARCHIVE}/csv" "${ARCHIVE}/other"
n_logs=0; n_csv=0; n_other=0

move_safe() {            # never overwrite: on a name clash, prefix the time so both copies are kept
  local src="$1" dest_dir="$2" base target
  base="$(basename "$src")"; target="${dest_dir}/${base}"
  [ -e "$target" ] && target="${dest_dir}/$(date +%H%M%S)_${base}"
  mv -- "$src" "$target"
}

for f in "${TARGET_DIR}"/*; do
  [ -f "$f" ] || continue
  [ "$(basename "$f")" = "$SELF" ] && continue          # never move this script itself
  case "$f" in
    *.log) move_safe "$f" "${ARCHIVE}/logs";   n_logs=$((n_logs +
1)) ;;
    *.csv) move_safe "$f" "${ARCHIVE}/csv";     n_csv=$((n_csv +
1)) ;;
    *)     move_safe "$f" "${ARCHIVE}/other"; n_other=$((n_other +
1)) ;;
  esac
done

echo "Organised into ${ARCHIVE}: logs=${n_logs} csv=${n_csv}
other=${n_other}"
```

> 📁 Saved as [`code/organize.sh`](code/organize.sh)


### Step 4: Make it executable and test it


```bash
chmod +x organize.sh
touch test1.log test2.log "my file.log" test3.csv notes.txt ./organize.sh .
ls -R archive_*
```

Expected summary line: Organized into ./archive_YYYY-MM-DD: logs=3 csv=1 other=1. The script itself (organize.sh) must not have been moved.
Now test the name-clash protection: create another file called test1.log and run ./organize.sh . again. Both copies must survive, the new one with a time prefix.

### Step 5: Explain the error handling

The comments in the script explain `set -euo` pipefail: exit on error (-e), exit on an unset variable (-u), and fail a pipeline if any stage fails (pipefail). Read them, then add one comment of your own describing what the move_safe function protects against.

## Required outcomes / tasks

- [ ] organize.sh submitted along with a terminal screenshot of a successful run (system clock visible), showing the per-category counts.
- [ ] Extend the script with a fourth category (for example *.json into a json/ folder) and update the summary line; submit the modified script.
- [ ] Short written answer: what happens if `set -euo pipefail` is removed and the script hits an error midway? Give one example for each flag.

## Code files in this lab

- [`code/organize.sh`](code/organize.sh)
