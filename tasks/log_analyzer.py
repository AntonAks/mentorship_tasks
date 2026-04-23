"""
Задача 1: Аналізатор логів

Формат рядка логу:
    2026-04-20 08:12:33 ERROR Database connection timeout

Реалізуй функції нижче. Не змінюй їх сигнатури.
"""
from pathlib import Path
from pydantic import BaseModel


class LogEntry(BaseModel):
    datetime: str
    level: str
    message: str


def parse_log_line(line: str) -> LogEntry:
    """
    Парсить один рядок логу.

    Повертає LogEntry з полями:
        datetime — дата і час у форматі "2026-04-20 08:12:33"
        level    — рівень логу (ERROR, WARNING, INFO тощо)
        message  — повідомлення (все після рівня)
    """
    parts = line.strip().split(" ", 3)
    return LogEntry(
        datetime=f"{parts[0]} {parts[1]}",
        level=parts[2],
        message=parts[3],
    )


def count_by_level(logs: list[LogEntry]) -> dict:
    """
    Приймає список LogEntry.
    Повертає словник {рівень: кількість}, наприклад:
        {"INFO": 5, "WARNING": 2, "ERROR": 3}
    """
    counts: dict[str, int] = {}
    for log in logs:
        counts[log.level] = counts.get(log.level, 0) + 1
    return counts


def most_error_hour(logs: list[LogEntry]) -> int:
    """
    Повертає годину (0–23) з найбільшою кількістю логів рівня ERROR.
    Якщо ERROR немає — повертає -1.
    """
    hour_counts: dict[int, int] = {}
    for log in logs:
        if log.level == "ERROR":
            hour = int(log.datetime[11:13])
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
    return max(hour_counts, key=lambda h: hour_counts[h]) if hour_counts else -1


def generate_report(filepath: str) -> str:
    """
    Читає файл логів, парсить кожен рядок і повертає текстовий звіт.

    Звіт має містити:
    - Загальну кількість логів
    - Кількість по кожному рівню
    - Годину з найбільшою кількістю помилок

    Формат довільний, головне — інформація присутня.
    """
    lines = Path(filepath).read_text().splitlines()
    logs = [parse_log_line(line) for line in lines if line.strip()]
    counts = count_by_level(logs)
    peak = most_error_hour(logs)

    report_lines = [f"Total logs: {len(logs)}"]
    for level, count in sorted(counts.items()):
        report_lines.append(f"{level}: {count}")
    report_lines.append(f"Peak error hour: {peak}")

    return "\n".join(report_lines)
