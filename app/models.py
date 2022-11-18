from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager
from sqlalchemy import DateTime
from datetime import datetime
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64))
    fullname = db.Column(db.String(64))
    phone = db.Column(db.String(10))
    dob = db.Column(db.Date())
    #Create Enum for Gender
    gender = db.Column(db.Boolean, default=False)
    #ballance = db.Column(db.Integer)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)


    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    #Mot User co nhieu Address
    addresses = db.relationship('Address', backref='users')
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Address(db.Model):
    __tablename__='addresses'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String())
    city  = db.Column(db.String())
    area  = db.Column(db.String())
    postal_code  = db.Column(db.String())
    country  = db.Column(db.String())
    is_default = db.Column(db.Boolean(), default=False)
    #Mot Address thuoc ve mot User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Category(db.Model):
    __tablename__= 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), unique=True, index=True)
    # Mot Category co nhieu san pham
    products = db.relationship('Product', backref='categories')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64), index=True)
    product_img = db.Column(db.String())
    product_subimg1 = db.Column(db.String())
    product_subimg2 = db.Column(db.String())
    product_subimg3 = db.Column(db.String())
    price = db.Column(db.Float)
    desc = db.Column(db.String())
    tag = db.Column(db.String())
    # Mot san pham co nhieu size 
    sizes = db.relationship('StockAndSize', backref='products')
    # Mot San pham thuoc ve mot Category
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

class StockAndSize(db.Model):
    __tablename__ = 'product_stock'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), index=True)
    size = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    # UniqueConstraint('product_id', 'size', name='size_product')
    
class BannerImage(db.Model):
    __tablename__='banner_images'
    id = db.Column(db.Integer, primary_key=True)
    banner = db.Column(db.String())
    is_disable = db.Column(db.Boolean(), default=False)
    
#Mot size thuoc ve mot San Pham
    
# class Voucher
#     #mot User co nhieu voucher
#     #mot Order ap dung mot voucher

# class Order
#     # 1 User co nhieu Order
#     # 1 Order co nhieu Product

# class Cart
#     # 1 User co mot Cart
#     # 1 Cart co nhieu Product

# class History
#     # 1 user co mot History
#     # 1 History chua nhieu Order







