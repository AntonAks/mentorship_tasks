"""
Задача 1: Аналізатор логів

Формат рядка логу:
    2026-04-20 08:12:33 ERROR Database connection timeout

Реалізуй функції нижче. Не змінюй їх сигнатури.
"""
import json
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
    ...


def count_by_level(logs: list[LogEntry]) -> dict:
    """
    Приймає список LogEntry.
    Повертає словник {рівень: кількість}, наприклад:
        {"INFO": 5, "WARNING": 2, "ERROR": 3}
    """
    ...


def most_error_hour(logs: list[LogEntry]) -> int:
    """
    Повертає годину (0–23) з найбільшою кількістю логів рівня ERROR.
    Якщо ERROR немає — повертає -1.
    """
    ...


def generate_report(filepath: str) -> str:
    """
    Читає файл логів, парсить кожен рядок і повертає текстовий звіт.

    Звіт має містити:
    - Загальну кількість логів
    - Кількість по кожному рівню
    - Годину з найбільшою кількістю помилок

    Формат довільний, головне — інформація присутня.
    """
    ...

