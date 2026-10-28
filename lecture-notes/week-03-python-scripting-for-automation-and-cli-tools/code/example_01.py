import argparse, sys
p = argparse.ArgumentParser(description="Summarise a log file")
p.add_argument("path")
p.add_argument("--top", type=int, default=5, help="how many items to show")
args = p.parse_args()
print(f"Reading {args.path}, top {args.top}")
