# 🐍 Python Junior Tasks

Практичні задачі для прокачки навичок Python.

## Як працювати

1. Зроби форк цього репозиторію
2. Створи нову гілку для кожної задачі: `task-1-log-analyzer`, `task-2-contacts`, `task-3-csv-compare`
3. Реалізуй рішення у відповідному файлі в папці `tasks/`
4. Створи Pull Request — тести запустяться автоматично
5. Всі тести мають бути зеленими ✅

## Задачі

### Задача 1: Аналізатор логів (`tasks/log_analyzer.py`)

Є текстовий файл з логами сервера у форматі:

```
2026-04-20 08:12:33 ERROR Database connection timeout
2026-04-20 08:12:35 INFO Retrying connection...
2026-04-20 08:13:01 WARNING Disk usage above 80%
```

Реалізуй функції:

- `parse_log_line(line: str) -> dict` — парсить один рядок логу, повертає словник з ключами: `datetime`, `level`, `message`
- `count_by_level(logs: list[dict]) -> dict` — рахує кількість логів кожного рівня
- `most_error_hour(logs: list[dict]) -> int` — повертає годину (0–23) з найбільшою кількістю ERROR
- `generate_report(filepath: str) -> str` — читає файл, повертає текстовий звіт

---

### Задача 2: Менеджер контактів (`tasks/contact_manager.py`)

Реалізуй клас `ContactManager` з методами:

- `add_contact(name: str, phone: str, email: str) -> None` — додає контакт, валідує дані
- `search(query: str) -> list[dict]` — шукає за ім'ям (часткове співпадіння, без урахування регістру)
- `delete_contact(name: str) -> bool` — видаляє контакт за точним ім'ям, повертає `True` якщо знайдено
- `save(filepath: str) -> None` — зберігає контакти в JSON
- `load(filepath: str) -> None` — завантажує контакти з JSON

Валідація:
- Email має містити `@` і `.` після `@`
- Телефон — тільки цифри, мінімум 10 символів
- При невалідних даних — кидати `ValueError` з описом помилки

---

### Задача 3: Порівнювач цін (`tasks/price_comparator.py`)

Є два CSV-файли від різних постачальників з колонками: `product_name,price,in_stock`

Реалізуй функції:

- `read_catalog(filepath: str) -> dict` — читає CSV, повертає словник `{product_name: {"price": float, "in_stock": bool}}`
- `find_common_products(catalog_a: dict, catalog_b: dict) -> list[str]` — список спільних товарів
- `find_cheaper(catalog_a: dict, catalog_b: dict) -> list[dict]` — для кожного спільного товару: `{"product": name, "price_a": ..., "price_b": ..., "cheaper": "A" | "B" | "same"}`
- `find_exclusive(catalog_a: dict, catalog_b: dict) -> dict` — `{"only_a": [...], "only_b": [...]}`
- `export_report(cheaper: list[dict], exclusive: dict, filepath: str) -> None` — записує результат у CSV

---

## Запуск тестів локально

```bash
pip install pytest
pytest -v
```

## Структура

```
├── .github/workflows/tests.yml
├── tasks/
│   ├── log_analyzer.py        # ← твій код тут
│   ├── contact_manager.py     # ← твій код тут
│   └── price_comparator.py    # ← твій код тут
├── tests/
│   ├── test_log_analyzer.py
│   ├── test_contact_manager.py
│   └── test_price_comparator.py
├── test_data/
│   └── ...
└── README.md
```
