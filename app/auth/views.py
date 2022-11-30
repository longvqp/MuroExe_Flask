from flask import render_template, flash, redirect, url_for, request
from .forms import RegistrationForm, LoginForm, InformationForm, AddressForm
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, Address, Cart, Product, Order, CartItem, Role
from ..import db

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username==form.username.data.lower()) \
                                    | (User.email==form.username.data.lower())).first()
        # user = User.query.filter_by(username=form.username.data.lower()).first()
        print(user.role)
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if user.is_user():
                    next = url_for('main.index')
                else:
                    next = url_for('admin.manage')
            return redirect(next)
            
        flash('Invalid user or password.')
    return render_template('auth/login.html',form=form)


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name='User').first()
        print(role)
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data,
                    role=role)
        db.session.add(user)
        db.session.commit()
        print(user)
        flash('Register complete!, Login to fill in more data')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/infor', methods=['GET','POST'])
def infor():
    inforForm = InformationForm()
    print(current_user.id)
    if inforForm.validate_on_submit():
        current_user.fullname = inforForm.fullname.data
        current_user.phone = inforForm.phone.data
        current_user.dob = inforForm.dob.data
        db.session.commit()
        flash("Information updated")

    return render_template('user/account_infor.html', inforForm=inforForm)


@auth.route('/address', methods=['GET','POST'])
def address():
    addressForm = AddressForm()
    if addressForm.validate_on_submit():    
        new_address = Address(address=addressForm.address.data,
        city=addressForm.city.data,
        postal_code=addressForm.postal_code.data,
        country = addressForm.country.data,
        user_id = current_user.id)
        db.session.add(new_address)
        db.session.commit()
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    print("Addres:",len(addresses))
    return render_template('user/account_address.html', addressForm=addressForm, addresses=addresses)

@auth.route('/delete_address/<address_id>', methods=['GET','POST'])
def delete_address(address_id):
    is_deleted = Address.query.filter_by(id=address_id).delete()
    db.session.commit()
    flash('Deleted Address')
    return redirect(url_for('auth.address'))

@auth.route('/make_default/<address_id>', methods=['GET','POST'])
def make_address_default(address_id):
    #Check if have other default
    default_address = Address.query.filter_by(is_default=True).first()
    if( default_address ):
        default_address.is_default=False
        db.session.commit()
    else:
        address = Address.query.filter_by(id=address_id).first()
        address.is_default=True
        db.session.commit()
        flash(address.address + ' is now default address')
    return redirect(url_for('auth.address'))

@auth.route('/adding_address', methods=['GET','POST'])
def adding_address():
    addressForm = AddressForm()
    if addressForm.validate_on_submit():    
        new_address = Address(address=addressForm.address.data,
        city=addressForm.city.data,
        postal_code=addressForm.postal_code.data,
        country = addressForm.country.data,
        user_id = current_user.id)

        db.session.add(new_address)

        db.session.commit()
        flash('Added new address')
        return redirect(url_for('auth.address'))
    return render_template('user/add_address.html',addressForm=addressForm)

@auth.route('/voucher')
def voucher():
    return render_template('user/account_voucher.html')

@auth.route('/history')
def history():
    return render_template('user/account_history.html')

@auth.route('/cart', methods=['GET','POST'])
def GetCart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    cart_items = CartItem.query.filter_by(cart_id=cart.id)
    print("sdljablfjasnl",len(cart_items.all()))
    return render_template('user/user_cart.html',cart_items=cart_items)

@auth.route('/check_out', methods=['GET','POST'])
def CheckOut():

    return render_template('user/user_order.html')