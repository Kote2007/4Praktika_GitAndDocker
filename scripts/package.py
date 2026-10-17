import os
import shutil
import sys
from pathlib import Path

REQUIRED_FILES = [
    "attendance.py",
    "README.md",
    "Dockerfile",
    "attendance.csv.example",
]


def main() -> int:
    dist = Path("dist")

    if dist.exists():
        shutil.rmtree(dist)

    dist.mkdir(parents=True)

    for name in REQUIRED_FILES:
        src = Path(name)

        if not src.exists():
            print(f"Missing required file: {src}", file=sys.stderr)
            return 1

        shutil.copy2(src, dist / src.name)

    files = sorted(
        p.name
        for p in dist.iterdir()
        if p.is_file() and p.name != "manifest.txt"
    )

    manifest_lines = [
        f"commit: {os.environ.get('GITHUB_SHA', 'unknown')}",
        f"pipeline: {os.environ.get('GITHUB_RUN_ID', 'unknown')}",
        "files:",
    ]

    manifest_lines.extend(files)

    manifest_path = dist / "manifest.txt"
    manifest_path.write_text(
        "\n".join(manifest_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Created dist with {len(files)} files")
    print(manifest_path.read_text(encoding="utf-8"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())