from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired


class EditAdvertForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    submit = SubmitField('Сохранить')