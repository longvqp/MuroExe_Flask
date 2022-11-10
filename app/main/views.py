from flask import render_template
from . import main
from ..models import Product

@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html',products=products)


@main.route('/product/<product_id>')
def product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if( not product):
        return render_template('error/404.html'), 404
    
    return render_template('product/products.html',product=product)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/infor/<user_id>', methods=['GET','POST'])
def get_infor(user_id): 
    return render_template('account_infor.html', user_id=user_id)


@main.route('/listing/<category>', methods=['GET','POST'])
def listing(category):
    print(category)
    return render_template('listing.html')