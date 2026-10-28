# Lab 3: Command-Line Tools with Python (argparse)

**Course:** DFSP-5208  |  **Lecture week:** 3  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Build a reusable command-line utility using the free, built-in `argparse` module.
- Accept input file paths, flags, and options from the terminal instead of hard-coding them.
- Package the tool so classmates can run it with `--help` to see usage instructions.

## Short theory

Hard-coded scripts (Lab 2) are useful once; command-line tools are reusable. argparse, included with every Python installation at no cost, turns a script into a small program with named options, default values, and automatic `--help` text, the same pattern used by professional forensic tooling. This lab converts the CSV filter built in Lab 2 into a flexible CLI utility.
Real tools also report what they do. Python's `logging` module (standard library) writes timestamped messages with a severity level, which is far more useful than print statements; Lab 12 returns to it in depth. This lab also begins the Git habit: every lab from now on ends with a commit.

## Prerequisites

- Lab 2 completed.
- sample_data.csv from Lab 2 (or regenerate it).
- Git installed and configured (Lab 1, Step 7).

## Step-by-step solution


### Step 1: Create the CLI script

Create log_filter_cli.py accepting --input, --output, --level and --limit arguments. The corrected version counts the rows it writes in a plain loop; an earlier draft printed “0 rows written” because writer.writerow() returns the number of characters written, not None.

```python
#!/usr/bin/env python3
"""Filter a CSV of log records by level. Usage: log_filter_cli.py --input IN --output OUT [--level L] [--limit N]"""
import argparse, csv, logging, sys
from pathlib import Path

logging.basicConfig(level=logging.INFO,
format="%(asctime)s %(levelname)s %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Filter CSV records by log level.")
    parser.add_argument("--input", required=True, help="Path to source CSV")
    parser.add_argument("--output", required=True, help="Path to write filtered CSV")
    parser.add_argument("--level", default="ERROR", choices=["INFO", "WARN", "ERROR"], help="Level to keep")
    parser.add_argument("--limit", type=int, default=0, help="Stop after N matching rows (0 = no limit)")
    args = parser.parse_args()

    src, dst = Path(args.input), Path(args.output)
    if not src.exists():
        logging.error("Input file not found: %s", src)
        return 1
    dst.parent.mkdir(parents=True, exist_ok=True)

    written = skipped = 0
    with src.open(newline="", encoding="utf-8") as inp, dst.open("w", newline="", encoding="utf-8") as out:
        reader = csv.DictReader(inp)
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
        writer.writeheader()
        for line_no, row in enumerate(reader, start=2):       # line 1 is the header
            level = row.get("level")
            if level is None:
                skipped += 1
                logging.warning("line %d skipped: no 'level' column value", line_no)
                continue
            if level == args.level:
                writer.writerow(row)
                written += 1
                if args.limit and written >= args.limit:
                    break
    print(f"{written} rows with level={args.level} written to {dst} ({skipped} skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

> 📁 Saved as [`code/log_filter_cli.py`](code/log_filter_cli.py)


### Step 2: Run with --help


```bash
python log_filter_cli.py --help
```


### Step 3: Run against the sample data


```bash
python log_filter_cli.py --input ../lab02/sample_data.csv --output warn_only.csv --level WARN
python log_filter_cli.py --input ../lab02/sample_data.csv --output out/warn3.csv --level WARN --limit 3
python log_filter_cli.py --input nope.csv --output x.csv; echo "exit code: $?"   # message and exit code 1
```

The count printed on the last line must equal the number of data rows in the output file (wc -l minus the header line).

### Step 4: Make the script executable (Linux/macOS)

The script already starts with the shebang line #!/usr/bin/env python3. Mark the file executable so it can be called directly, similar to a native command-line tool.

```bash
chmod +x log_filter_cli.py
./log_filter_cli.py --input ../lab02/sample_data.csv --output warn_only.csv --level WARN
```


### Step 5: Document the extra flag and commit

Document the --limit option in a short README.md and commit the lab to Git.

```text
# log_filter_cli
Filters a CSV of log records by level.

    python3 log_filter_cli.py --input IN.csv --output OUT.csv [--level INFO|WARN|ERROR] [--limit N]

--limit N   stop after N matching rows (default 0 = no limit)
```

> 📁 Saved as [`code/README.md`](code/README.md)


```bash
cd ~/forensic-scripting/lab03
git init
git add log_filter_cli.py README.md
git commit -m "Lab 3: argparse CLI with --limit"
```


## Required outcomes / tasks

- [ ] log_filter_cli.py submitted with a screenshot of the --help output (system clock visible).
- [ ] Output CSV files for both ERROR and WARN levels, and the printed count matching `wc -l` minus one.
- [ ] README.md documenting --limit, plus one additional optional flag of your own choice (e.g. --host NAME).
- [ ] Screenshot of `git log --oneline` showing at least one commit for this lab.

## Code files in this lab

- [`code/README.md`](code/README.md)
- [`code/log_filter_cli.py`](code/log_filter_cli.py)
