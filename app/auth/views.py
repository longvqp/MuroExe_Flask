from flask import render_template
from .forms import RegistrationForm
from . import auth

@auth.route('/login', methods=['GET','SET'])
def login():
    return render_template('auth/login.html')


@auth.route('/register', methods=['GET','SET'])
def register():
    form = RegistrationForm()
    return render_template('auth/register.html',form = form)