from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Category
from .. import db

class AddProductForm(FlaskForm):
    product_name = StringField('Product Name: ', validators=[DataRequired()])
    product_img = FileField('Product Image: ', validators=[DataRequired()])
    category = SelectField('Category', choices=[('shoes', 'Shoe'), ('boots', 'Boot'), ('slippers', 'Slipper')])
    submit = SubmitField()