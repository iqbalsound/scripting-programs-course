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
