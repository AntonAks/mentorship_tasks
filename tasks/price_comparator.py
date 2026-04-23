"""
Задача 3: Порівнювач цін з CSV

Формат CSV-файлу:
    product_name,price,in_stock
    Laptop,999.99,true
    Mouse,25.50,false

Реалізуй функції нижче. Не змінюй їх сигнатури.
"""

import csv


def read_catalog(filepath: str) -> dict:
    """
    Читає CSV-файл каталогу.
    Повертає словник:
        {
            "Laptop": {"price": 999.99, "in_stock": True},
            "Mouse": {"price": 25.50, "in_stock": False},
        }
    """
    pass


def find_common_products(catalog_a: dict, catalog_b: dict) -> list[str]:
    """
    Повертає відсортований список товарів, які є в обох каталогах.
    """
    pass


def find_cheaper(catalog_a: dict, catalog_b: dict) -> list[dict]:
    """
    Для кожного спільного товару повертає порівняння:
        {
            "product": "Laptop",
            "price_a": 999.99,
            "price_b": 1099.99,
            "cheaper": "A"  # або "B" або "same"
        }
    Список відсортований за product.
    """
    pass


def find_exclusive(catalog_a: dict, catalog_b: dict) -> dict:
    """
    Повертає товари, які є тільки в одного постачальника:
        {
            "only_a": ["Keyboard", ...],
            "only_b": ["Webcam", ...]
        }
    Списки відсортовані.
    """
    pass


def export_report(cheaper: list[dict], exclusive: dict, filepath: str) -> None:
    """
    Записує результат порівняння у CSV-файл з колонками:
        product,price_a,price_b,cheaper

    Спочатку — рядки з cheaper (спільні товари).
    Потім — ексклюзивні товари only_a з price_b порожнім і cheaper="A only".
    Потім — ексклюзивні товари only_b з price_a порожнім і cheaper="B only".
    """
    pass
