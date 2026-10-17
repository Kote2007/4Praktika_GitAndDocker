import sys
from pathlib import Path


def main() -> int:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "deploy/test")

    if not target.is_dir():
        print(f"Deployment target not found: {target}", file=sys.stderr)
        return 1

    sys.path.insert(0, str(target.resolve()))

    try:
        import attendance
    except Exception as exc:
        print(
            f"Cannot import attendance from {target}: {exc}",
            file=sys.stderr,
        )
        return 1

    if hasattr(attendance, "duration_minutes"):
        result = attendance.duration_minutes("23:30", "00:15")
    else:
        records = []
        attendance.register_entry(records, "Полюс", "23:30")
        attendance.register_exit(records, "Полюс", "00:15")
        result = attendance.calculate_duration(records, "Полюс")

    if result != 45:
        print(
            f"Smoke check failed: expected 45, got {result}",
            file=sys.stderr,
        )
        return 1

    print("Smoke check passed: duration across midnight =", result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())