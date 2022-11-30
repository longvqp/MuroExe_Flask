from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField,DateField, PasswordField, \
    BooleanField, SubmitField, SelectField, IntegerField, TextAreaField,FloatField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .. import db


class AddEmployeeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])

    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    
    role = SelectField('Role', choices=[('Warehouse Manager', 'Warehouse Manager'), \
                        ('Sales Employee', 'Sales Employee'), ('Shipper', 'Shipper')])
    role1 = SelectField('Role', choices=[('Manager', 'Manager'),('Warehouse Manager', 'Warehouse Manager'), \
                        ('Sales Employee', 'Sales Employee'), ('Shipper', 'Shipper')])
    submit = SubmitField('Add Employee')
class EditEmployeeForm(FlaskForm):
    email = StringField('Email')
    username = StringField('Username')
    fullname = StringField('Full name')
    phone = StringField('Phone number: ')
    dob = DateField('Your Dob: ')
    gender = BooleanField()
    role = SelectField('Role', choices=[('Warehouse Manager', 'Warehouse Manager'), \
                        ('Sales Employee', 'Sales Employee'), ('Shipper', 'Shipper')])
    role1 = SelectField('Role', choices=[('Manager', 'Manager'),('Warehouse Manager', 'Warehouse Manager'), \
                        ('Sales Employee', 'Sales Employee'), ('Shipper', 'Shipper')])
    submit = SubmitField('Update')

