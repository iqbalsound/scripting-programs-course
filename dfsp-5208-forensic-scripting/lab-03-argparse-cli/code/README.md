# log_filter_cli
Filters a CSV of log records by level.

    python3 log_filter_cli.py --input IN.csv --output OUT.csv [--level INFO|WARN|ERROR] [--limit N]

--limit N   stop after N matching rows (default 0 = no limit)
