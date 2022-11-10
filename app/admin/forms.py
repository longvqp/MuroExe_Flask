from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Category
from .. import db

class AddProductForm(FlaskForm):
    product_name = StringField('Product Name: ', validators=[DataRequired()])
    product_img = FileField('Product Image: ', validators=[DataRequired()])
    product_subimg1 = FileField('Product Sub Image 1: ', validators=[DataRequired()])
    product_subimg2 = FileField('Product Sub Image 2: ', validators=[DataRequired()])
    product_subimg3 = FileField('Product Sub Image 3: ', validators=[DataRequired()])
    price = IntegerField('Price')
    desc = TextAreaField('Product Description')

    category = SelectField('Category', choices=[('shoes', 'Shoe'), ('boots', 'Boot'), ('slippers', 'Slipper')])
    submit = SubmitField()