from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField,FloatField
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
    price = IntegerField('Price', validators=[DataRequired()])
    desc = TextAreaField('Product Description')
    category = SelectField('Category', choices=[('shoes', 'Shoe'), ('boots', 'Boot'), ('slippers', 'Slipper')])
    submit = SubmitField('Add Product')

class EditProductForm(FlaskForm):
    product_name = StringField('Product Name: ', validators=[DataRequired()])
    price = FloatField('Price')
    desc = TextAreaField('Product Description')
    category = SelectField('Category', choices=[('shoes', 'Shoe'), ('boots', 'Boot'), ('slippers', 'Slipper')])
    tag = SelectField('Tag', choices=[('New Arrival', 'New Arrival'), ('Best Seller', 'Best Seller'),('None', 'None')])
    submit = SubmitField('Update Product')

class AddStockForm(FlaskForm):
    size = IntegerField('Size: ')
    stock = IntegerField('In Stock: ')
    submit = SubmitField('Add Size')

class UpdateStockForm(FlaskForm):
    stock = IntegerField('In Stock: ')
    submit = SubmitField('Update')

class AddBannerImageForm(FlaskForm):
    banner = FileField('Product Image: ', validators=[DataRequired()])
    is_disable = BooleanField('Disalbe')
    submit = SubmitField('save')