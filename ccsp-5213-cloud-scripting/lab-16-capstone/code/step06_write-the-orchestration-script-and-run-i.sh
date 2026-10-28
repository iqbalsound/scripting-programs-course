#!/usr/bin/env bash
# Cloud capstone orchestrator: stops at the first failure; logs each stage with a UTC timestamp.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data out
log() { echo "$(date -u +%FT%TZ) $*" | tee -a out/pipeline.log; }

log "[1/5] Filtering usage data"
python3 scripts/log_filter_cli.py --input data/usage.csv --output data/filtered.csv --level WARN
log "[2/5] Checking budgets"
python3 scripts/check_budgets.py data/filtered.csv data/scan_result.json
log "[3/5] Alerting if over budget"
python3 scripts/alert_from_scan.py data/scan_result.json
ARCHIVE="out/archive_$(date -u +%Y%m%d_%H%M%S).tar.gz"
log "[4/5] Archiving"
tar -czf "$ARCHIVE" data/
sha256sum "$ARCHIVE" >> out/SHA256SUMS
if [ -n "${S3_URL:-}" ]; then                         # skipped when no S3 endpoint is configured
  log "[5/5] Uploading to the S3 endpoint"
  python3 scripts/upload_to_s3.py "$ARCHIVE"
fi
log "Pipeline complete: $ARCHIVE"
