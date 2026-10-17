from datetime import datetime, timedelta

LATE_MINUTES = 10
START_TIME = "09:00"


def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M")


def duration_minutes(entry_time, exit_time):
    start = parse_time(entry_time)
    end = parse_time(exit_time)

    if end < start:
        return end - start

    delta = end - start
    return int(delta.total_seconds() // 60)


def calculate_duration(records, name):
    for record in reversed(records):
        if record["name"] == name and record["exit"] is not None:
            record["duration_minutes"] = duration_minutes(
                record["entry"],
                record["exit"]
            )
            return record["duration_minutes"]

    raise ValueError("Закрытая запись не найдена")


def register_entry(records, name, entry_time):
    record = {
        "name": name,
        "entry": entry_time,
        "exit": None,
        "duration_minutes": None,
        "late": is_late(entry_time),
    }
    records.append(record)
    return record


def register_exit(records, name, exit_time):
    for record in reversed(records):
        if record["name"] == name and record["exit"] is None:
            record["exit"] = exit_time
            return record

    raise ValueError("Запись для выхода не найдена")


def is_late(entry_time, start_time=START_TIME, late_minutes=LATE_MINUTES):
    entry_dt = parse_time(entry_time)
    start_dt = parse_time(start_time)
    delta = entry_dt - start_dt

    return int(delta.total_seconds() // 60) >= late_minutes


def main():
    print("Запущена прога для отслеживания посещений")

    records = []

    register_entry(records, "Котэ", "09:00")
    register_entry(records, "Нитроген", "09:15")
    register_entry(records, "Полюс", "23:30")

    register_exit(records, "Котэ", "10:30")
    register_exit(records, "Нитроген", "11:00")
    register_exit(records, "Полюс", "00:15")

    print("Список посещений:")
    for r in records:
        print(r)

    print("Длительность посещения Сони:", calculate_duration(records, "Полюс"))
    print("А дальше кода нет :3")


if __name__ == "__main__":
    main()