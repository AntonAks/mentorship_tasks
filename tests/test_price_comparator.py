import csv
import pytest
from pathlib import Path
from tasks.price_comparator import (
    read_catalog,
    find_common_products,
    find_cheaper,
    find_exclusive,
    export_report,
)

DATA_DIR = Path(__file__).parent / ".." / "test_data"
SUPPLIER_A = DATA_DIR / "supplier_a.csv"
SUPPLIER_B = DATA_DIR / "supplier_b.csv"


class TestReadCatalog:
    def test_reads_all_products(self):
        catalog = read_catalog(SUPPLIER_A)
        assert len(catalog) == 6

    def test_price_is_float(self):
        catalog = read_catalog(SUPPLIER_A)
        assert isinstance(catalog["Laptop"]["price"], float)
        assert catalog["Laptop"]["price"] == 999.99

    def test_in_stock_is_bool(self):
        catalog = read_catalog(SUPPLIER_A)
        assert catalog["Laptop"]["in_stock"] is True
        assert catalog["Monitor"]["in_stock"] is False

    def test_product_names_correct(self):
        catalog = read_catalog(SUPPLIER_A)
        assert "Mouse" in catalog
        assert "USB Cable" in catalog


class TestFindCommonProducts:
    def test_common_products(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        common = find_common_products(cat_a, cat_b)
        assert sorted(common) == ["Headphones", "Keyboard", "Laptop", "Mouse"]

    def test_result_is_sorted(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        common = find_common_products(cat_a, cat_b)
        assert common == sorted(common)

    def test_no_common_products(self):
        cat_a = {"ItemA": {"price": 10.0, "in_stock": True}}
        cat_b = {"ItemB": {"price": 20.0, "in_stock": True}}
        assert find_common_products(cat_a, cat_b) == []


class TestFindCheaper:
    def test_laptop_cheaper_at_a(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        cheaper = find_cheaper(cat_a, cat_b)
        laptop = next(item for item in cheaper if item["product"] == "Laptop")
        assert laptop["price_a"] == 999.99
        assert laptop["price_b"] == 1099.99
        assert laptop["cheaper"] == "A"

    def test_mouse_cheaper_at_b(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        cheaper = find_cheaper(cat_a, cat_b)
        mouse = next(item for item in cheaper if item["product"] == "Mouse")
        assert mouse["cheaper"] == "B"

    def test_keyboard_same_price(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        cheaper = find_cheaper(cat_a, cat_b)
        keyboard = next(item for item in cheaper if item["product"] == "Keyboard")
        assert keyboard["cheaper"] == "same"

    def test_result_is_sorted(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        cheaper = find_cheaper(cat_a, cat_b)
        products = [item["product"] for item in cheaper]
        assert products == sorted(products)

    def test_result_has_correct_keys(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        cheaper = find_cheaper(cat_a, cat_b)
        for item in cheaper:
            assert set(item.keys()) == {"product", "price_a", "price_b", "cheaper"}


class TestFindExclusive:
    def test_only_a(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        exclusive = find_exclusive(cat_a, cat_b)
        assert sorted(exclusive["only_a"]) == ["Monitor", "USB Cable"]

    def test_only_b(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        exclusive = find_exclusive(cat_a, cat_b)
        assert sorted(exclusive["only_b"]) == ["Desk Lamp", "Webcam"]

    def test_results_are_sorted(self):
        cat_a = read_catalog(SUPPLIER_A)
        cat_b = read_catalog(SUPPLIER_B)
        exclusive = find_exclusive(cat_a, cat_b)
        assert exclusive["only_a"] == sorted(exclusive["only_a"])
        assert exclusive["only_b"] == sorted(exclusive["only_b"])


class TestExportReport:
    def test_creates_file(self, tmp_path):
        cheaper = [
            {"product": "Laptop", "price_a": 999.99, "price_b": 1099.99, "cheaper": "A"},
        ]
        exclusive = {"only_a": ["USB Cable"], "only_b": ["Webcam"]}
        filepath = str(tmp_path / "report.csv")
        export_report(cheaper, exclusive, filepath)
        assert Path(filepath).exists()

    def test_csv_has_header(self, tmp_path):
        cheaper = [
            {"product": "Laptop", "price_a": 999.99, "price_b": 1099.99, "cheaper": "A"},
        ]
        exclusive = {"only_a": [], "only_b": []}
        filepath = str(tmp_path / "report.csv")
        export_report(cheaper, exclusive, filepath)

        with open(filepath) as f:
            reader = csv.reader(f)
            header = next(reader)
        assert "product" in header
        assert "price_a" in header
        assert "price_b" in header
        assert "cheaper" in header

    def test_csv_contains_common_products(self, tmp_path):
        cheaper = [
            {"product": "Laptop", "price_a": 999.99, "price_b": 1099.99, "cheaper": "A"},
            {"product": "Mouse", "price_a": 25.50, "price_b": 22.00, "cheaper": "B"},
        ]
        exclusive = {"only_a": [], "only_b": []}
        filepath = str(tmp_path / "report.csv")
        export_report(cheaper, exclusive, filepath)

        with open(filepath) as f:
            content = f.read()
        assert "Laptop" in content
        assert "Mouse" in content

    def test_csv_contains_exclusive_products(self, tmp_path):
        cheaper = []
        exclusive = {"only_a": ["USB Cable"], "only_b": ["Webcam"]}
        filepath = str(tmp_path / "report.csv")
        export_report(cheaper, exclusive, filepath)

        with open(filepath) as f:
            content = f.read()
        assert "USB Cable" in content
        assert "A only" in content
        assert "Webcam" in content
        assert "B only" in content
