#!/usr/bin/env bash
dir="$1"; days="${2:-7}"
[ -d "$dir" ] || { echo "Not a directory: $dir" >&2; exit 1; }
find "$dir" -type f -mtime +"$days" -print
