"""
Задача 2: Менеджер контактів

Реалізуй клас ContactManager з методами нижче.
Не змінюй сигнатури методів.

Валідація:
- Email: має містити '@' і '.' після '@'
- Телефон: тільки цифри, мінімум 10 символів
- При невалідних даних — ValueError з описом
"""

import json


class ContactManager:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name: str, phone: str, email: str) -> None:
        """
        Додає контакт до списку.
        Кидає ValueError якщо phone або email невалідні.
        """
        pass

    def search(self, query: str) -> list[dict]:
        """
        Шукає контакти за ім'ям.
        Часткове співпадіння, без урахування регістру.
        Повертає список знайдених контактів.
        """
        pass

    def delete_contact(self, name: str) -> bool:
        """
        Видаляє контакт за точним ім'ям (без урахування регістру).
        Повертає True якщо контакт знайдено і видалено, False якщо ні.
        """
        pass

    def save(self, filepath: str) -> None:
        """Зберігає self.contacts у JSON-файл."""
        pass

    def load(self, filepath: str) -> None:
        """Завантажує контакти з JSON-файлу в self.contacts."""
        pass
