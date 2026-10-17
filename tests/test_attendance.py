import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from attendance import (
    calculate_duration,
    duration_minutes,
    is_late,
    parse_time,
    register_entry,
    register_exit,
)


class TestParseTime(unittest.TestCase):
    def test_parse_time_valid(self):
        dt = parse_time("09:05")
        self.assertEqual(dt.strftime("%H:%M"), "09:05")

    def test_parse_time_invalid(self):
        bad_values = [
            "25:00",
            "09:60",
            "ab:cd",
            "",
        ]

        for value in bad_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_time(value)


class TestDurationMinutes(unittest.TestCase):
    def test_duration_same_day(self):
        self.assertEqual(duration_minutes("09:00", "10:30"), 90)

    def test_duration_crosses_midnight(self):
        self.assertEqual(duration_minutes("23:30", "00:15"), 45)

    def test_duration_equal_times(self):
        self.assertEqual(duration_minutes("10:00", "10:00"), 0)

    def test_duration_one_minute_crossing_midnight(self):
        self.assertEqual(duration_minutes("23:59", "00:00"), 1)


class TestIsLate(unittest.TestCase):
    def test_nine_minutes_is_not_late(self):
        self.assertFalse(is_late("09:09"))

    def test_ten_minutes_is_late(self):
        self.assertTrue(is_late("09:10"))

    def test_before_start_is_not_late(self):
        self.assertFalse(is_late("08:55"))


class TestRegisterEntry(unittest.TestCase):
    def test_register_entry_creates_open_record(self):
        records = []
        record = register_entry(records, "Котэ", "09:00")

        self.assertEqual(len(records), 1)
        self.assertEqual(record["name"], "Котэ")
        self.assertEqual(record["entry"], "09:00")
        self.assertIsNone(record["exit"])
        self.assertIsNone(record["duration_minutes"])
        self.assertFalse(record["late"])

    def test_register_entry_marks_late(self):
        records = []
        record = register_entry(records, "Нитроген", "09:15")

        self.assertTrue(record["late"])


class TestRegisterExit(unittest.TestCase):
    def test_register_exit_closes_open_record(self):
        records = []
        register_entry(records, "Котэ", "09:00")
        record = register_exit(records, "Котэ", "10:30")

        self.assertEqual(record["exit"], "10:30")

    def test_register_exit_raises_if_no_open_record(self):
        records = []
        register_entry(records, "Котэ", "09:00")
        register_exit(records, "Котэ", "10:30")

        with self.assertRaises(ValueError):
            register_exit(records, "Котэ", "11:00")


class TestCalculateDuration(unittest.TestCase):
    def test_calculate_duration_for_closed_record(self):
        records = []
        register_entry(records, "Котэ", "09:00")
        register_exit(records, "Котэ", "10:30")

        duration = calculate_duration(records, "Котэ")

        self.assertEqual(duration, 90)
        self.assertEqual(records[-1]["duration_minutes"], 90)

    def test_calculate_duration_crosses_midnight(self):
        records = []
        register_entry(records, "Полюс", "23:30")
        register_exit(records, "Полюс", "00:15")

        duration = calculate_duration(records, "Полюс")

        self.assertEqual(duration, 45)

    def test_calculate_duration_raises_if_no_closed_record(self):
        records = []
        register_entry(records, "Котэ", "09:00")

        with self.assertRaises(ValueError):
            calculate_duration(records, "Котэ")


if __name__ == "__main__":
    unittest.main()