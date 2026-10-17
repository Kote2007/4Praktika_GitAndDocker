import sys
from pathlib import Path

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "deploy",
}

SKIP_BINARY = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".exe",
    ".dll",
    ".so",
    ".pyc",
}

bad_files = []

for path in Path(".").rglob("*"):
    if not path.is_file():
        continue

    if any(part in SKIP_DIRS for part in path.parts):
        continue

    if path.suffix.lower() in SKIP_BINARY:
        continue

    try:
        path.read_text(encoding="utf-8")
    except Exception as exc:
        bad_files.append(f"{path}: {exc}")

if bad_files:
    print("UTF-8 check failed:")
    for line in bad_files:
        print(line)
    sys.exit(1)

print("UTF-8 check OK")