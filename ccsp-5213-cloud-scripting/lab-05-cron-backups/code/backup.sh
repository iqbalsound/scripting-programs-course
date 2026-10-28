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
