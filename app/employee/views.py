from flask import render_template, current_app as app, redirect,url_for,flash
from . import employee
from .forms import AddEmployeeForm, EditEmployeeForm
from ..models import User, Role
from .. import db
from flask_login import current_user, login_required
from functools import wraps

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (current_user.role.permission & 63) < 16:
            flash("Bạn không có quyền truy cập!")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@employee.route('/list')
@login_required
@is_admin
def listEmployee():
    users = User.query.join(Role).all()
    userList = [user for user in users if user.role.permission < current_user.role.permission]
    return render_template('employees/list.html', users=userList)

    
@employee.route('/add_employee', methods=['GET','POST'])
@login_required
@is_admin
def AddEmployee():
    form = AddEmployeeForm()
    if form.is_submitted():
        if current_user.role.permission > 16:
            role = Role.query.filter_by(name=form.role1.data).first()
        else:
            role = Role.query.filter_by(name=form.role.data).first()
        user = User(email=form.email.data.lower(),
                    password=form.password.data,
                    role=role,
                    confirmed=True)
        db.session.add(user)
        db.session.commit()
        flash('Add complete!')
        return redirect(url_for('employee.listEmployee'))
 
    return render_template('employees/add_employee.html', form=form, curUser=current_user )

@employee.route('/edit_employee/<id>', methods=['GET','POST'])
@is_admin
def editEmployee(id):
    user = User.query.get(id)
    editForm = EditEmployeeForm()
    if editForm.is_submitted():
        role = Role.query.filter_by(name=editForm.role.data).filter_by(name=editForm.role1.data).first()
        user.username = editForm.username.data
        user.fullname =  editForm.fullname.data
        user.phone =  editForm.phone.data
        user.dob =  editForm.dob.data
        user.gender = editForm.gender.data
        user.role = role
        db.session.commit()
        return redirect(url_for('employee.listEmployee'))   
    return render_template('employees/edit_employee.html', form=editForm, user=user, curUser= current_user)

@employee.route('/delete_employee/<id>')
def deleteEmployee(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('employee.listEmployee')) 

