

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange
import uuid
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'


class BookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired(), Length(min=1, max=100)])
    author = StringField('Autor', validators=[DataRequired(), Length(min=1, max=100)])
    year = IntegerField('Rok wydania', validators=[DataRequired(), NumberRange(min=0, max=2100)])
    description = TextAreaField('Opis', validators=[Length(max=500)])


class DeleteForm(FlaskForm):
    pass


BOOKS_FILE = 'books.json'


def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_books(books):
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


@app.route('/', methods=['GET', 'POST'])
def index():
    books = load_books()
    form = BookForm()
    delete_form = DeleteForm()

    if form.validate_on_submit():
        new_book = {
            'id': str(uuid.uuid4()),
            'title': form.title.data,
            'author': form.author.data,
            'year': form.year.data,
            'description': form.description.data
        }
        books.append(new_book)
        save_books(books)
        return redirect(url_for('index'))

    return render_template('index.html', books=books, form=form, delete_form=delete_form)


@app.route('/delete/<book_id>', methods=['POST'])
def delete_book(book_id):
    form = DeleteForm()
    if form.validate_on_submit():
        books = load_books()
        books = [b for b in books if b['id'] != book_id]
        save_books(books)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
