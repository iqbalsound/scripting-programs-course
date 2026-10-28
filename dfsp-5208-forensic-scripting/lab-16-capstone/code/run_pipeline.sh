#!/usr/bin/env bash
# Capstone orchestrator: stops at the first failure and logs each stage with a UTC timestamp.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data out
log() { echo "$(date -u +%FT%TZ) $*" | tee -a out/pipeline.log; }

log "[1/4] Filtering raw logs"
python3 scripts/log_filter_cli.py --input data/raw.csv --output data/filtered.csv --level ERROR

log "[2/4] Scanning for IOC matches"
if [ -n "${SCAN_URL:-}" ]; then                      # production: the faasd function, e.g. http://host.docker.internal:8080/function/ioc-alert
  curl -fsS -X POST "$SCAN_URL" --data-binary @data/filtered.csv > data/scan_result.json
else                                                 # no faasd available: run the same handler through the local harness
  node faas/harness.js faas/handler.js "$(cat data/filtered.csv)" > data/scan_result.json
fi

log "[3/4] Sending alert if matches found"
python3 scripts/alert_from_scan.py data/scan_result.json

log "[4/4] Archiving results"
ARCHIVE="out/archive_$(date -u +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$ARCHIVE" data/
sha256sum "$ARCHIVE" >> out/SHA256SUMS
log "Pipeline complete: $ARCHIVE"
