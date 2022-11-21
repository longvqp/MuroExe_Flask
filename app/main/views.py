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
       

   
    print(products)
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

