from flask import render_template, flash, redirect, url_for, request
from .forms import RegistrationForm, LoginForm, InformationForm, AddressForm, OrderForm
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, Address, Cart, Product, Order, CartItem
from ..import db

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
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
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data
                    )
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
    if(cart):
        cart_items = CartItem.query.filter_by(cart_id=cart.id)
       
    else:
        new_cart = Cart(user_id=current_user.id)
        db.session.add(new_cart)
        db.session.commit()
    return render_template('user/user_cart.html',cart_items=cart_items,cart=cart)

@auth.route('/checkout_address', methods=['GET','POST'])
def CheckOutAddress():
    order_form = OrderForm()
    total=0
    item_count=0
    discount = float(-10)
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    cart_items = CartItem.query.filter_by(cart_id=cart.id)
    for pd in cart_items:
        # print(pd.product.price)
        # print(pd.quantity)
        item_count += pd.quantity
        price_per_product = float(pd.product.price) * int(pd.quantity)
        total += price_per_product
    final_price = total + discount
    
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    
    param_address = request.args.get('address_id')
    chosen_address = Address.query.filter_by(id=param_address).first()

    return render_template('user/user_order_address.html',form=order_form,cart_items=cart_items,total=total,item_count=item_count,final_price=final_price,discount=discount,addresses=addresses,chosen_address=chosen_address)

@auth.route('/checkout_address/set/<address_id>', methods=['GET','POST'])
def SetOrderAddress(address_id):
    return redirect(url_for('auth.CheckOutAddress',address_id=address_id))


@auth.route('/place_order', methods=['GET','POST'])
def PlaceOrder():
    order_form = OrderForm()
    if order_form.validate_on_submit():
        print("email",order_form.email.data)
        print("full name",order_form.fullname.data)
        print("phone",order_form.phone.data)
        print("payment",order_form.payment.data)
        print("address id",order_form.address.data)
        print("cart id",order_form.cart_id.data)
        print("total money",order_form.total.data)
    return render_template('user/user_order_payment.html')
        
@auth.route('/checkout_payment', methods=['GET','POST'])
def CheckOutPayment():
    # cart = Cart.query.filter_by(user_id=current_user.id).first()
    return render_template('user/user_order_payment.html')