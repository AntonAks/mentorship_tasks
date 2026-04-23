import pytest
from pathlib import Path
from tasks.log_analyzer import LogEntry, parse_log_line, count_by_level, most_error_hour, generate_report

SAMPLE_LOGS_PATH = Path(__file__).parent / ".." / "test_data" / "sample_logs.txt"


class TestParseLogLine:
    def test_basic_error(self):
        result = parse_log_line("2026-04-20 08:12:33 ERROR Database connection timeout")
        assert result.datetime == "2026-04-20 08:12:33"
        assert result.level == "ERROR"
        assert result.message == "Database connection timeout"

    def test_info_log(self):
        result = parse_log_line("2026-04-20 09:00:00 INFO Server started")
        assert result.datetime == "2026-04-20 09:00:00"
        assert result.level == "INFO"
        assert result.message == "Server started"

    def test_warning_log(self):
        result = parse_log_line("2026-04-20 08:13:01 WARNING Disk usage above 80%")
        assert result.level == "WARNING"
        assert result.message == "Disk usage above 80%"

    def test_message_with_special_chars(self):
        result = parse_log_line("2026-04-20 10:00:00 ERROR Connection refused: port=5432")
        assert result.message == "Connection refused: port=5432"

    def test_returns_logentry_instance(self):
        result = parse_log_line("2026-04-20 08:12:33 ERROR Test")
        assert isinstance(result, LogEntry)


class TestCountByLevel:
    def test_mixed_levels(self):
        logs = [
            LogEntry(datetime="2026-04-20 08:00:00", level="ERROR", message="a"),
            LogEntry(datetime="2026-04-20 08:00:01", level="ERROR", message="b"),
            LogEntry(datetime="2026-04-20 08:00:02", level="INFO", message="c"),
            LogEntry(datetime="2026-04-20 08:00:03", level="WARNING", message="d"),
        ]
        result = count_by_level(logs)
        assert result["ERROR"] == 2
        assert result["INFO"] == 1
        assert result["WARNING"] == 1

    def test_single_level(self):
        logs = [
            LogEntry(datetime="2026-04-20 08:00:00", level="INFO", message="a"),
            LogEntry(datetime="2026-04-20 08:00:01", level="INFO", message="b"),
        ]
        result = count_by_level(logs)
        assert result["INFO"] == 2
        assert result.get("ERROR", 0) == 0

    def test_empty_list(self):
        result = count_by_level([])
        assert result == {} or all(v == 0 for v in result.values())


class TestMostErrorHour:
    def test_clear_winner(self):
        logs = [
            LogEntry(datetime="2026-04-20 10:00:00", level="ERROR", message="a"),
            LogEntry(datetime="2026-04-20 10:01:15", level="ERROR", message="b"),
            LogEntry(datetime="2026-04-20 10:02:30", level="ERROR", message="c"),
            LogEntry(datetime="2026-04-20 08:12:33", level="ERROR", message="d"),
            LogEntry(datetime="2026-04-20 09:00:00", level="INFO", message="e"),
        ]
        assert most_error_hour(logs) == 10

    def test_no_errors(self):
        logs = [
            LogEntry(datetime="2026-04-20 09:00:00", level="INFO", message="a"),
        ]
        assert most_error_hour(logs) == -1

    def test_single_error(self):
        logs = [
            LogEntry(datetime="2026-04-20 14:35:10", level="ERROR", message="a"),
        ]
        assert most_error_hour(logs) == 14

    def test_ignores_non_error_levels(self):
        logs = [
            LogEntry(datetime="2026-04-20 08:00:00", level="WARNING", message="a"),
            LogEntry(datetime="2026-04-20 08:00:01", level="WARNING", message="b"),
            LogEntry(datetime="2026-04-20 08:00:02", level="WARNING", message="c"),
            LogEntry(datetime="2026-04-20 10:00:00", level="ERROR", message="d"),
        ]
        assert most_error_hour(logs) == 10


class TestGenerateReport:
    def test_report_contains_total(self):
        report = generate_report(SAMPLE_LOGS_PATH)
        assert "15" in report  # total log count

    def test_report_contains_error_count(self):
        report = generate_report(SAMPLE_LOGS_PATH)
        # 6 errors in sample file
        assert "6" in report

    def test_report_contains_peak_hour(self):
        report = generate_report(SAMPLE_LOGS_PATH)
        assert "10" in report  # hour 10 has 3 errors

    def test_report_is_nonempty_string(self):
        report = generate_report(SAMPLE_LOGS_PATH)
        assert isinstance(report, str)
        assert len(report) > 20
