from flask import render_template, current_app as app, redirect,url_for,flash
from . import admin
from .forms import AddProductForm,EditProductForm,AddStockForm,UpdateStockForm
from ..models import Product, Category, StockAndSize
from .. import db
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from config import config

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/add_product', methods=['GET','POST'])
def AddProduct():
    form = AddProductForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        
        print("CO CHAY NGE")
        category = Category.query.filter_by(category_name=form.category.data).first()
        uploaded_picture = form.product_img.data
        uploaded_sub_picture1 = form.product_subimg1.data
        uploaded_sub_picture2 = form.product_subimg2.data
        uploaded_sub_picture3 = form.product_subimg3.data
        print(form.product_name.data)
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
        
        product_subimg2_name = str(uuid.uuid1()) + "_" + uploaded_sub_picture2_name
        uploaded_sub_picture2.save(os.path.join(app.config['UPLOAD_FOLDER'], product_subimg2_name))
        
        product_subimg3_name = str(uuid.uuid1()) + "_" + uploaded_sub_picture3_name
        uploaded_sub_picture3.save(os.path.join(app.config['UPLOAD_FOLDER'], product_subimg3_name))
        
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
 
    return render_template('admin/add_product.html', form=form)

@admin.route('/manage_product', methods=['GET','POST'])
def ManageProduct():
    products = Product.query.all()
    return render_template('admin/manage_product.html', products=products)


@admin.route('/delete/<product_id>', methods=['GET','POST'])
def DeleteProduct(product_id):
    is_deleted = Product.query.filter_by(id=product_id).delete()
    db.session.commit()
    return redirect(url_for('admin.ManageProduct'))

@admin.route('/edit_for/<product_id>', methods=['GET','POST'])
def EditProduct(product_id):


     
    product = Product.query.filter_by(id=product_id).first()
    editForm = EditProductForm()
    if editForm.validate_on_submit():
        product.product_name = editForm.product_name.data
        product.price = editForm.price.data
        product.desc = editForm.desc.data 
        db.session.commit()
        return redirect(url_for('admin.ManageProduct'))   
    return render_template('admin/edit_product.html', product=product, form=editForm)
   
@admin.route('/check_stock/<product_id>', methods=['GET','POST'])
def CheckStock(product_id):
    product = Product.query.filter_by(id=product_id).first()
    sizes = StockAndSize.query.filter_by(product_id=product_id)
    stockForm = AddStockForm()
    updateForm = UpdateStockForm()
    if stockForm.validate_on_submit():
        print("STOCK FORM SUBMIT")
        size_exist = StockAndSize.query.filter_by(size=stockForm.size.data,product_id=product.id).first()
        
        if( not size_exist):
            stock = StockAndSize(size=stockForm.size.data,
                                    stock=stockForm.stock.data,
                                    product_id=product.id)
            db.session.add(stock)
            db.session.commit()
        else:
            flash("Size Exist")
            return redirect(url_for('admin.CheckStock',product_id=product.id))   
    if updateForm.validate_on_submit():
        print("UPDATING STOCK VALUE")
    return render_template('admin/product_stock.html', product=product,sizes=sizes,form=stockForm, updateForm=updateForm)

@admin.route('/update_stock/<product_id>', methods=['POST'])
def UpdateStock(product_id):
    product = Product.query.filter_by(id=product_id).first()
    updateForm = UpdateStockForm()
    if updateForm.validate_on_submit():
        
        print("FORM WORKING")
    return redirect(url_for('admin.CheckStock',product_id=product.id))   


