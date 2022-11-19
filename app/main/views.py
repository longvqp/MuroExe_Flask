from flask import render_template,request
from . import main
from ..models import Product,StockAndSize,Category,BannerImage
from sqlalchemy import desc,asc
@main.route('/')
def index():
    products = Product.query.all()
    banners = BannerImage.query.all()
    return render_template('index.html',products=products,banners=banners)


@main.route('/product/<product_id>')
def product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    stock_size = StockAndSize.query.filter_by(product_id=product_id).all()
    if( not product):
        return render_template('error/404.html'), 404
    
    return render_template('product/products.html',product=product,stock_size=stock_size)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/infor/<user_id>', methods=['GET','POST'])
def get_infor(user_id): 
    return render_template('account_infor.html', user_id=user_id)


@main.route('/listing/<category>', methods=['GET','POST'])
def listing(category):
    sort = request.args.get('sort')
    ctgr = Category.query.filter_by(category_name=category).first()
    products = Product.query.filter_by(category_id=ctgr.id)
    
    if(sort=='r_alpha'):
        products = products.order_by(desc(Product.product_name)).all()
    if(sort=='alpha'):
        products = products.order_by(asc(Product.product_name)).all()
    if(sort=='price_asc'):
        products = products.order_by(asc(Product.price)).all()
    if(sort=='price_desc'):
        products = products.order_by(desc(Product.price)).all()
    return render_template('product/listing.html', products = products,ctgr=ctgr)

