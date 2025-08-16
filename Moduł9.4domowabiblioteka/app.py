from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

BOOKS_FILE = 'books.json'


def load_books():
    """Ładowanie książek z pliku JSON"""
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_books(books):
    """Zapisywanie książek do pliku JSON"""
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)




@app.route('/api/books', methods=['GET'])
def api_get_books():
    return jsonify(load_books()), 200


@app.route('/api/books/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
    books = load_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404


@app.route('/api/books', methods=['POST'])
def api_add_book():
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data or 'year' not in data or 'pages' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    books = load_books()
    new_id = max([b['id'] for b in books], default=0) + 1
    new_book = {
        'id': new_id,
        'title': data['title'],
        'author': data['author'],
        'year': data['year'],
        'pages': f"{data['pages']} str",
        'description': data.get('description', '')
    }
    books.append(new_book)
    save_books(books)
    return jsonify(new_book), 201


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def api_delete_book(book_id):
    books = load_books()
    new_books = [b for b in books if b['id'] != book_id]
    if len(new_books) == len(books):
        return jsonify({'error': 'Book not found'}), 404
    save_books(new_books)
    return jsonify({'message': 'Book deleted'}), 200



@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')


if __name__ == '__main__':
    app.run(debug=True)

