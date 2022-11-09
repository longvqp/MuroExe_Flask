from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/product')
def product():
    return render_template('products.html')

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