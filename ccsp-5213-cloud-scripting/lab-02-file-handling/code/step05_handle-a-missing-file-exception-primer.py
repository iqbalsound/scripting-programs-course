from pathlib import Path

src = Path("sample_data.csv")
try:
    text = src.read_text(encoding="utf-8")
except FileNotFoundError:
    raise SystemExit(f"Input file not found: {src}")
print(f"{len(text.splitlines())} lines read from {src}")
