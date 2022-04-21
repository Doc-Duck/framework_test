from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from Httpapp import db, apps
from Httpapp.models import Items, User


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
        print(price)
        db.session.add(items)
        db.session.commit()
        return redirect('viewer')
    else:
        return render_template('adprod.html')


@apps.route('/viewer')
@login_required
def viewer():
    items = Items.query.order_by(Items.id).all()
    return render_template("viewer.html", items=items)
