
from flask import Flask, request, jsonify
from models import load_books, save_books

app = Flask(__name__)


@app.route("/books", methods=["GET"])
def get_books():
    books = load_books()
    return jsonify(books), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def add_book():
    books = load_books()
    data = request.get_json()

    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_id = max([b["id"] for b in books], default=0) + 1
    new_book = {
        "id": new_id,
        "title": data.get("title"),
        "author": data.get("author"),
        "year": data.get("year", 0),
        "pages": data.get("pages", 0),
        "description": data.get("description", ""),
        "genre": data.get("genre", "")
    }

    books.append(new_book)
    save_books(books)
    return jsonify(new_book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    for field in ["title", "author", "year", "pages", "description", "genre"]:
        if field in data:
            book[field] = data[field]

    save_books(books)
    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    save_books(books)
    return jsonify({"message": "Book deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)




