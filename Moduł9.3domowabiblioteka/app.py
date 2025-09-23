


from flask import Flask, render_template_string, redirect, url_for
from models import load_books, save_books
from forms import BookForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "tajny_klucz"  # wymagany do WTForms


@app.route("/", methods=["GET", "POST"])
def homepage():
    books = load_books()
    form = BookForm()

    if form.validate_on_submit():
        new_id = max([b["id"] for b in books], default=0) + 1
        new_book = {
            "id": new_id,
            "title": form.title.data,
            "author": form.author.data,
            "year": form.year.data,
            "pages": form.pages.data,
            "description": form.description.data,
            "genre": form.genre.data,
        }
        books.append(new_book)
        save_books(books)
        return redirect(url_for("homepage"))

    # szablon osadzony w kodzie (można też użyć pliku HTML w templates/)
    html = """
    <h1>Domowa Biblioteka</h1>

    <h2>Dodaj książkę</h2>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.title.label }} {{ form.title(size=30) }}<br>
        {{ form.author.label }} {{ form.author(size=30) }}<br>
        {{ form.year.label }} {{ form.year() }}<br>
        {{ form.pages.label }} {{ form.pages() }}<br>
        {{ form.description.label }} {{ form.description(rows=3, cols=30) }}<br>
        {{ form.genre.label }} {{ form.genre(size=20) }}<br>
        {{ form.submit() }}
    </form>

    <h2>Lista książek</h2>
    <ul>
    {% for book in books %}
        <li>
            {{ book.title }} - {{ book.author }} ({{ book.year }}) | {{ book.pages }}
            <form action="{{ url_for('delete_book', book_id=book.id) }}" method="POST" style="display:inline;">
                <button type="submit">Usuń</button>
            </form>
        </li>
    {% endfor %}
    </ul>
    """
    return render_template_string(html, form=form, books=books)


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

