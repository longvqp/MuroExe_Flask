from flask import render_template, current_app as app, redirect,url_for,flash
from . import admin
from .forms import AddProductForm,EditProductForm,AddStockForm,UpdateStockForm,AddBannerImageForm
from ..models import Product, Category, StockAndSize, BannerImage
from .. import db
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import json
from config import config

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/add_product', methods=['GET','POST'])
def AddProduct():
    form = AddProductForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
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

@admin.route('/manage_product/<category>', methods=['GET','POST'])
def ManageProduct(category):
    ctgr = Category.query.filter_by(category_name=category).first()
    products = Product.query.filter_by(category_id=ctgr.id).all()
    return render_template('admin/manage_product.html', products=products)

@admin.route('/delete/<product_id>', methods=['GET','POST'])
def DeleteProduct(product_id):
    is_deleted = Product.query.filter_by(id=product_id).delete()
    db.session.commit()
    return redirect(url_for('admin.ManageProduct',category='shoes'))

@admin.route('/edit_for/<product_id>', methods=['GET','POST'])
def EditProduct(product_id):
    product = Product.query.filter_by(id=product_id).first()
    ctgr = Category.query.filter_by(id=product.category_id).first()
    print(ctgr.category_name)
    editForm = EditProductForm()
    if editForm.validate_on_submit():
        product.product_name = editForm.product_name.data
        product.price = editForm.price.data
        product.tag = editForm.tag.data 
        db.session.commit()
        return redirect(url_for('admin.ManageProduct',category=ctgr.category_name))   
    return render_template('admin/edit_product.html', product=product, form=editForm,ctgr=ctgr)
   
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

@admin.route('/update_stock/<size_id>', methods=['POST'])
def UpdateStock(size_id):
    stock = StockAndSize.query.filter_by(id=size_id).first()
    product = Product.query.filter_by(id=stock.product_id).first()
    updateForm = UpdateStockForm()
    if updateForm.validate_on_submit():
        stock.stock = updateForm.stock.data
        db.session.commit()
        print(stock.stock)
        print(updateForm.stock.data)
        print("FORM WORKING")
    return "Updated"
    # return redirect(url_for('admin.CheckStock',product_id=product.id))   

@admin.route('/banner_page', methods=['GET','POST'])
def PageBanner():
    banners = BannerImage.query.all()
    addbannerForm = AddBannerImageForm()
    if addbannerForm.validate_on_submit():
        banner_image_name = str(uuid.uuid1()) + "_" + secure_filename(addbannerForm.banner.data.filename)
        addbannerForm.banner.data.save(os.path.join(app.config['UPLOAD_FOLDER']+'/Banner', banner_image_name))
        banner = BannerImage(
            banner = banner_image_name,
            is_disable = addbannerForm.is_disable.data
        )
        db.session.add(banner)
        db.session.commit()
    return render_template('admin/page_banner.html',banners=banners, addbannerForm = addbannerForm)




# For Batch Data Adding
@admin.route('/add_category')
def AddCategory():
    shoe = Category(category_name='shoes')
    sneaker = Category(category_name='sneakers')
    boot = Category(category_name='boots')
    slipper = Category(category_name='slippers')
    accessory = Category(category_name='accessories')
    db.session.add_all([shoe,sneaker,boot,slipper,accessory])
    db.session.commit()
    flash("Added all category")
    return redirect(url_for('admin.index'))

@admin.route('/add_batch')
def AddBatch():
    datadir = "/Users/longvu/Projects/Moroexe_Flask/app/static/data"
    datas = []
    img_names = []
    with os.scandir(datadir) as folders:
        for folder in folders:
            if(folder.name!='.DS_Store'):
                #print("In Folder: "+folder.name)
                folderPath = (folder.path)
                for file in os.scandir(folderPath):
                    if( file!='.DS_Store' ):
                        #print(file)
                        if(file.name=='infor.JSON'):
                            with open(file, 'r') as fcc_file:
                                datas.append(json.load(fcc_file)) 


    # print (datas[1])
    
    for data in datas:
        category = Category.query.filter_by(category_name=(data['category'])).first()
        pd_name = (data['product_name'])
        pd_price = (data['price'])
        pd_desc = (data['desc'])
        img_1 = (data['product_img'])
        img_2 = (data['product_subimg1'])
        img_3 = (data['product_subimg2'])
        img_4 = (data['product_subimg3'])
        product = Product(product_name = pd_name,
                            price = pd_price,
                            desc = pd_desc,
                            product_img = img_1,
                            product_subimg1 = img_2,
                            product_subimg2 = img_3,
                            product_subimg3 = img_4,
                            categories=category
                            )
        db.session.add(product)
        db.session.commit()
    flash("Added a bunch of data")
    return redirect(url_for('admin.index'))
