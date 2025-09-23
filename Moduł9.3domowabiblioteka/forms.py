
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class BookForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    author = StringField("Autor", validators=[DataRequired()])
    year = IntegerField("Rok wydania", validators=[DataRequired(), NumberRange(min=0)])
    pages = IntegerField("Liczba stron", validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField("Opis")
    genre = StringField("Gatunek")
    submit = SubmitField("Dodaj książkę")
