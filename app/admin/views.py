from flask import render_template, current_app as app
from . import admin
from .forms import AddProductForm
from ..models import Product, Category
from .. import db
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from config import config


@admin.route('/', methods=['GET','POST'])
def index():
    
    form = AddProductForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(category_name=form.category.data).first()
        uploaded_picture = form.product_img.data
        

        uploaded_picture_name = secure_filename(form.product_img.data.filename)
        product_img_name = str(uuid.uuid1()) + "_" + uploaded_picture_name
        print(product_img_name)
        uploaded_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], product_img_name))
        
        # product = Product(product_name=form.product_name.data,
        #                     product_img=form.product_img.data,
        #                     categories=category)
        # db.session.add(product)
        # db.session.commit()
 
    return render_template('admin/index.html', form=form)

