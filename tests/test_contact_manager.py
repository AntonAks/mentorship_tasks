import json
import pytest
from pathlib import Path
from tasks.contact_manager import ContactManager


@pytest.fixture
def manager():
    return ContactManager()


@pytest.fixture
def populated_manager():
    m = ContactManager()
    m.add_contact("Olena Shevchenko", "0501234567", "olena@example.com")
    m.add_contact("Taras Kovalenko", "0677654321", "taras@work.ua")
    m.add_contact("Anna Bondarenko", "0931112233", "anna.b@gmail.com")
    return m


class TestAddContact:
    def test_add_valid_contact(self, manager):
        manager.add_contact("Test User", "0501234567", "test@example.com")
        assert len(manager.contacts) == 1
        assert manager.contacts[0]["name"] == "Test User"
        assert manager.contacts[0]["phone"] == "0501234567"
        assert manager.contacts[0]["email"] == "test@example.com"

    def test_add_multiple_contacts(self, manager):
        manager.add_contact("User One", "0501234567", "one@test.com")
        manager.add_contact("User Two", "0509876543", "two@test.com")
        assert len(manager.contacts) == 2

    def test_invalid_email_no_at(self, manager):
        with pytest.raises(ValueError):
            manager.add_contact("Test", "0501234567", "invalid-email.com")

    def test_invalid_email_no_dot_after_at(self, manager):
        with pytest.raises(ValueError):
            manager.add_contact("Test", "0501234567", "invalid@email")

    def test_invalid_phone_too_short(self, manager):
        with pytest.raises(ValueError):
            manager.add_contact("Test", "12345", "test@example.com")

    def test_invalid_phone_with_letters(self, manager):
        with pytest.raises(ValueError):
            manager.add_contact("Test", "050abc4567", "test@example.com")

    def test_invalid_phone_with_special_chars(self, manager):
        with pytest.raises(ValueError):
            manager.add_contact("Test", "+380501234567", "test@example.com")


class TestSearch:
    def test_search_full_name(self, populated_manager):
        results = populated_manager.search("Olena Shevchenko")
        assert len(results) == 1
        assert results[0]["name"] == "Olena Shevchenko"

    def test_search_partial_name(self, populated_manager):
        results = populated_manager.search("olen")
        assert len(results) == 1
        assert results[0]["name"] == "Olena Shevchenko"

    def test_search_case_insensitive(self, populated_manager):
        results = populated_manager.search("TARAS")
        assert len(results) == 1

    def test_search_multiple_results(self, populated_manager):
        # "en" matches "Olena Shevchenko" and "Anna Bondarenko"
        results = populated_manager.search("en")
        assert len(results) == 2

    def test_search_no_results(self, populated_manager):
        results = populated_manager.search("Nonexistent")
        assert results == []


class TestDeleteContact:
    def test_delete_existing(self, populated_manager):
        result = populated_manager.delete_contact("Olena Shevchenko")
        assert result is True
        assert len(populated_manager.contacts) == 2

    def test_delete_case_insensitive(self, populated_manager):
        result = populated_manager.delete_contact("olena shevchenko")
        assert result is True

    def test_delete_nonexistent(self, populated_manager):
        result = populated_manager.delete_contact("Ghost User")
        assert result is False
        assert len(populated_manager.contacts) == 3

    def test_delete_does_not_remove_others(self, populated_manager):
        populated_manager.delete_contact("Taras Kovalenko")
        names = [c["name"] for c in populated_manager.contacts]
        assert "Olena Shevchenko" in names
        assert "Anna Bondarenko" in names


class TestSaveLoad:
    def test_save_creates_file(self, populated_manager, tmp_path):
        filepath = str(tmp_path / "contacts.json")
        populated_manager.save(filepath)
        assert Path(filepath).exists()

    def test_save_valid_json(self, populated_manager, tmp_path):
        filepath = str(tmp_path / "contacts.json")
        populated_manager.save(filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 3

    def test_load_restores_contacts(self, populated_manager, tmp_path):
        filepath = str(tmp_path / "contacts.json")
        populated_manager.save(filepath)

        new_manager = ContactManager()
        new_manager.load(filepath)
        assert len(new_manager.contacts) == 3
        names = [c["name"] for c in new_manager.contacts]
        assert "Olena Shevchenko" in names
