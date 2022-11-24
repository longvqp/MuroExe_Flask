from flask import render_template,request,flash,redirect,url_for
from flask_login import current_user
from . import main
from ..models import Product,StockAndSize,Category,BannerImage,Cart
from .. import db
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
    category = Category.query.filter_by(id=product.category_id).first()
    products = Product.query.filter_by(category_id=category.id).all()
    if( not product):
        return render_template('error/404.html'), 404
    
    return render_template('product/products.html',product=product,stock_size=stock_size,category=category,products=products)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/infor/<user_id>', methods=['GET','POST'])
def get_infor(user_id): 
    return render_template('account_infor.html', user_id=user_id)


@main.route('/listing/<category>', methods=['GET','POST'])
def listing(category):
    sort = request.args.get('sort')
    get_color = request.args.get('color')
    get_style = request.args.get('style')

    ctgr = Category.query.filter_by(category_name=category).first()
    products = Product.query.filter_by(category_id=ctgr.id).all()
    pd_att = Product.query.filter_by(category_id=ctgr.id).all()
  
    if(get_color and get_style):
        products_forsorting = Product.query.filter_by(category_id=ctgr.id,color=get_color)
        products_forsorting = products_forsorting.filter(Product.style.contains(get_style))
        products = products_forsorting.all()
    else:
        products_forsorting = Product.query.filter_by(category_id=ctgr.id)
        if(get_color):
            products_forsorting = Product.query.filter_by(category_id=ctgr.id,color=get_color)
            products = products_forsorting.all()
        if(get_style):
            products_forsorting = Product.query.filter_by(category_id=ctgr.id)
            products_forsorting = products_forsorting.filter(Product.style.contains(get_style))
            products = products_forsorting.all()

    if(sort=='r_alpha'):
        products = products_forsorting.order_by(desc(Product.product_name)).all()
    if(sort=='alpha'):
        products = products_forsorting.order_by(asc(Product.product_name)).all()
    if(sort=='price_asc'):
        products = products_forsorting.order_by(asc(Product.price)).all()
    if(sort=='price_desc'):
        products = products_forsorting.order_by(desc(Product.price)).all()

    colors = []
    styles = []
    for pd in pd_att:
        if(pd.color!=''):
            colors.append(pd.color)
        if(pd.style!=''):
            styles.append(pd.style)
    colors = list(set(colors))
    styles = list(set(styles))
    style_ = []
    for style in styles:
        individual_style = style.split('\n')
        for i in individual_style:
            style_.append(i)
    style_ = list(set(style_))

    return render_template('product/listing.html', products = products,ctgr=ctgr,colors=colors,styles=style_)

#Trường hợp 2 User đều có một product trong giỏ hàng
#User đặt trước sẽ nhận được
#User chưa đặt thì thông báo sản phẩm hết hàng và xóa khỏi giỏ hàng
#
@main.route('/add_to_cart/<product_id>', methods=['GET','POST'])
def AddToCart(product_id):
    print(product_id)
    pd = Product.query.filter_by(id=product_id).first()
    quantity = request.args.get('quantity')
    size = request.args.get("size_input")
    print("size input", size)
    print("quantity", quantity)
    

    carts = Cart.query.filter_by(user_id=current_user.id).all()
    for cart in carts:
        print("All the product:",cart.product_incart)
        for pd_incart in cart.product_incart:
            print("Each Product:",pd_incart)
            print("Product ID:",pd_incart.id,'---',pd.id)
            print("Product Size:",cart.size,'---',size)
            if(str(pd_incart.id)==str(pd.id) and str(cart.size) == str(size)):
                cart.quantity = quantity
                db.session.commit()
                flash("Quantity updated in cart")
                return redirect(url_for('main.product',product_id=pd.id))
            
                
    cart = Cart(user_id=current_user.id,size=size,quantity=quantity)
    cart.product_incart.append(pd)
    db.session.add(cart)
    db.session.commit()
    flash("Added item to cart")
    return redirect(url_for('main.product',product_id=pd.id))
    return redirect(url_for('main.product',product_id=pd.id))

