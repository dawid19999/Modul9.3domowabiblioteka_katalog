

import json
import os

BOOKS_FILE = "books.json"


def load_books():
    """Ładuje listę książek z pliku JSON."""
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_books(books):
    """Zapisuje listę książek do pliku JSON."""
    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)
