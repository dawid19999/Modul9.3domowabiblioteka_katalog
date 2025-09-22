
from flask import Flask, request, redirect, url_for
from models import load_books, save_books

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def homepage():
    books = load_books()

    
    if request.method == "POST":
        new_id = max([b["id"] for b in books], default=0) + 1
        new_book = {
            "id": new_id,
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "year": int(request.form.get("year")),
            "pages": int(request.form.get("pages")),
            "description": request.form.get("description", ""),
            "genre": request.form.get("genre", "")
        }
        books.append(new_book)
        save_books(books)
        return redirect(url_for("homepage"))

    
    html = """
    <h1>Domowa Biblioteka</h1>

    <h2>Dodaj książkę</h2>
    <form method="POST">
        <label>Tytuł: <input type="text" name="title" required></label><br>
        <label>Autor: <input type="text" name="author" required></label><br>
        <label>Rok wydania: <input type="number" name="year" required></label><br>
        <label>Liczba stron: <input type="number" name="pages" required></label><br>
        <label>Opis: <textarea name="description"></textarea></label><br>
        <button type="submit">Dodaj książkę</button>
    </form>

    <h2>Lista książek</h2>
    <ul>
    """
    for book in books:
        html += f"""
        <li>
            {book['title']} - {book['author']} ({book['year']}) | {book['pages']}
            <form action="/delete/{book['id']}" method="POST" style="display:inline;">
                <button type="submit">Usuń</button>
            </form>
        </li>
        """
    html += "</ul>"
    return html


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        books.remove(book)
        save_books(books)
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    app.run(debug=True)


