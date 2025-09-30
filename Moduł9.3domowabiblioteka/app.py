


from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
import uuid
from utils import load_books, save_books  # <- import zamiast duplikacji

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'


class BookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired(), Length(min=1, max=100)])
    author = StringField('Autor', validators=[DataRequired(), Length(min=1, max=100)])
    year = IntegerField('Rok wydania', validators=[DataRequired(), NumberRange(min=0, max=2100)])
    description = TextAreaField('Opis', validators=[Length(max=500)])
    submit = SubmitField('Zapisz książkę')


class DeleteForm(FlaskForm):
    submit = SubmitField('Usuń')


@app.route('/', methods=['GET', 'POST'])
@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def index(book_id=None):
    books = load_books()
    delete_form = DeleteForm()

    if book_id:
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            return redirect(url_for('index'))
        form = BookForm(data=book)
    else:
        form = BookForm()

    if form.validate_on_submit():
        if book_id:
            
            book['title'] = form.title.data
            book['author'] = form.author.data
            book['year'] = form.year.data
            book['description'] = form.description.data
            
        else:
             
            if books:
                new_id = str(max(int(b["id"]) for b in books) + 1)
            
            else:
                new_id = "1"

            new_book = {
                'id': new_id,  
                'title': form.title.data,
                'author': form.author.data,
                'year': form.year.data,
                'description': form.description.data,
                'genre': '',
                'pages': 0    
            }
            books.append(new_book)

        save_books(books)
        return redirect(url_for('index'))

    return render_template(
        'index.html',
        books=books,
        form=form,
        delete_form=delete_form,
        editing_id=book_id
    )


@app.route('/delete/<book_id>', methods=['POST'])
def delete_book(book_id):
    books = load_books()
    books = [b for b in books if b['id'] != book_id]
    save_books(books)
    return redirect(url_for('index'))


@app.route('/api/books/<book_id>', methods=['PUT'])
def update_book_api(book_id):
    books = load_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return {"error": "Book not found"}, 404

    data = request.json
    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])
    book['year'] = data.get('year', book['year'])
    book['description'] = data.get('description', book['description'])
    save_books(books)
    return {"message": "Book updated", "book": book}, 200


if __name__ == '__main__':
    app.run(debug=True)


