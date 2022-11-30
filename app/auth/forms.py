from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
import pycountry

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
    DataRequired(), Length(1, 64)])
    # Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
    #            'Usernames must have only letters, numbers, dots or '
    #            'underscores')
    password = PasswordField('Password')
    submit = SubmitField('Login')

class InformationForm(FlaskForm):
    email = StringField('Email')
    username = StringField('Username')
    fullname = StringField('Full name')
    phone = StringField('Phone number: ')
    dob = DateField('Your Dob: ')
    gender = BooleanField()
    password = PasswordField('Old Password'
       )
    password2 = PasswordField('New Password')
    submit = SubmitField('Save')

class AddressForm(FlaskForm):
    address = StringField("Address")
    city = StringField("City")
    postal_code = StringField("Postal Code")
    country = SelectField('Country', choices=[(country.name, country.name) for country in pycountry.countries])
    submit = SubmitField('Add')

