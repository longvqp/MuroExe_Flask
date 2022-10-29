from flask import render_template
from .forms import RegistrationForm, LoginForm
from . import auth
from ..models import User
@auth.route('/login', methods=['GET','SET'])
def login():
    form = LoginForm()

    return render_template('auth/login.html',form=form)


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        print(user.email)
        
        
    return render_template('auth/register.html',form = form)
