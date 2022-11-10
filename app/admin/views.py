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
        uploaded_sub_picture1 = form.product_subimg1.data
        uploaded_sub_picture2 = form.product_subimg2.data
        uploaded_sub_picture3 = form.product_subimg3.data
        
        #Secure Product Picture Prevent Inject SQL Attck
        uploaded_picture_name = secure_filename(uploaded_picture.filename)
        uploaded_sub_picture1_name =  secure_filename(uploaded_sub_picture1.filename)
        uploaded_sub_picture2_name =  secure_filename(uploaded_sub_picture2.filename)
        uploaded_sub_picture3_name =  secure_filename(uploaded_sub_picture3.filename)

        #Set unique id to picture name and save
        product_img_name = str(uuid.uuid1()) + "_" + uploaded_picture_name
        uploaded_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], product_img_name))
        product_image_path = os.path.join(app.config['UPLOAD_FOLDER'], product_img_name)

        product_subimg1_name = str(uuid.uuid1()) + "_" + uploaded_sub_picture1_name
        uploaded_sub_picture1.save(os.path.join(app.config['UPLOAD_FOLDER'], product_subimg1_name))
        product_subimage1_path = os.path.join(app.config['UPLOAD_FOLDER'], product_subimg1_name)

        product_subimg2_name = str(uuid.uuid1()) + "_" + uploaded_sub_picture2_name
        uploaded_sub_picture2.save(os.path.join(app.config['UPLOAD_FOLDER'], product_subimg2_name))
        product_subimage2_path = os.path.join(app.config['UPLOAD_FOLDER'], product_subimg2_name)

        product_subimg3_name = str(uuid.uuid1()) + "_" + uploaded_sub_picture3_name
        uploaded_sub_picture3.save(os.path.join(app.config['UPLOAD_FOLDER'], product_subimg3_name))
        product_subimage3_path = os.path.join(app.config['UPLOAD_FOLDER'], product_subimg3_name)
        

        product = Product(product_name=form.product_name.data,
                            product_img=product_img_name,
                            product_subimg1=product_subimg1_name,
                            product_subimg2=product_subimg2_name,
                            product_subimg3=product_subimg3_name,
                            price = form.price.data,
                            desc = form.desc.data,
                            categories=category)
        db.session.add(product)
        db.session.commit()
 
    return render_template('admin/index.html', form=form)

