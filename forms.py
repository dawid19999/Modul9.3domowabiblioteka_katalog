from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class BookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired(), Length(max=200)])
    author = StringField('Autor', validators=[DataRequired(), Length(max=100)])
    year = IntegerField('Rok wydania', validators=[DataRequired(), NumberRange(min=0, max=2100)])
    description = TextAreaField('Opis', validators=[Length(max=500)])
