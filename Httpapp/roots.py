import flask_login
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from werkzeug.security import check_password_hash, generate_password_hash

from Httpapp import db, apps, manager
from Httpapp.models import Items, User ,List1 #list_add
from Httpapp.exelimport import new_table
from Httpapp.elementadd import new_element


@apps.route('/')
def index():
    return render_template('index.html')


@apps.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@apps.route('/register', methods=['POST', 'GET'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    is_Admin = request.form.get("is_Admin")
    if request.method == "POST":
        if not (login or password or password2):
            flash('Пожалуйств запоните поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html')


@apps.route('/login', methods=['POST', 'GET'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('addprod'))
        else:
            flash('Данные введены некорректно')
            redirect(url_for('login'))
    else:
        flash('Пожалуйста заполните поля авторизации')
        return render_template('login.html')
    return render_template('login.html')


@apps.route('/adprod', methods=['POST', 'GET'])
@login_required
def addprod():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        items = Items(name=name, price=price)
        db.session.add(items)
        db.session.commit()
        return redirect('viewer')
    else:
        return render_template('adprod.html')


@apps.route('/viewer', methods=['POST', 'GET'])
@login_required
def viewer():
    if request.method == 'POST':
        print(request.form['Карандаши'])
    items = Items.query.order_by(Items.id).all()
    return render_template("viewer.html", items=items)


@apps.route('/editviewer', methods=['POST', 'GET'])
@login_required
def editviewer():
    items = Items.query.order_by(Items.id).all()
    return render_template("editviewer.html", items=items)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@apps.route('/addtable', methods=['POST', 'GET'])
def addtable():
    if request.method == 'POST':
        route = request.form['route']
        sheetname = request.form['sheetname']
        new_table(rf'{ route }', f'{sheetname}')
    return render_template('addtable.html')


@apps.route("/update", methods=["POST"])
def update():
    updatedname = request.form.get("updatedname")
    beforename = request.form.get("beforename")
    updatedprice = request.form.get("updatedprice")
    beforeprice = request.form.get("beforeprice")
    student = Items.query.filter_by(name=beforename).first()
    student.name = updatedname
    student.price = updatedprice

    db.session.commit()
    return redirect("/viewer")



@apps.route("/List1")
@login_required
def list1():
	list1 = List1.query.all()
	return render_template("List1.html", List1=list1)


@apps.route('/test', methods=['POST', 'GET'])
@login_required
def test():
    if request.method == 'POST':
        type = request.form['type']
        value = request.form['value']
        action = request.form['action']
        print(type,value,action)
        new_element(type, value, action)
    return render_template("test.html")