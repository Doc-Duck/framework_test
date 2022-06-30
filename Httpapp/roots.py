import flask_login
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList
from wtforms.validators import DataRequired

from Httpapp import db, apps, manager
from Httpapp.models import Items, User, List1 ,Hehehaha #list_add
from Httpapp.exelimport import new_table, add_table
from Httpapp.elementadd import new_element, new_chart


class FavouriteMoviesForm(FlaskForm):
    table_name = StringField("Table name", validators=[DataRequired()])
    columns = FieldList(StringField('Column name'), min_entries=1, max_entries=100)


apps.config['SECRET_KEY'] = "hehehaha"


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
            return redirect(url_for('viewer'))
        else:
            flash('Данные введены некорректно')
            redirect(url_for('login'))
    else:
        flash('Пожалуйста заполните поля авторизации')
        return render_template('login.html')
    return render_template('login.html')


@apps.route('/viewer', methods=['POST', 'GET'])
@login_required
def viewer():
    if request.method == 'POST':
        type = request.form['type']
        column_x = request.form['column-x']
        column_y = request.form['column-y']
        file_name = request.form['file-name']
        print(file_name, type, column_x, column_y)
        new_chart(file_name, type, column_x, column_y)
    items = Items.query.order_by(Items.id).all()
    return render_template("viewer.html", items=items)


@apps.route('/adprod', methods=['POST'])
@login_required
def addprod():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        amount = request.form['amount']
        items = Items(name=name, price=price, amount=amount)
        db.session.add(items)
        db.session.commit()
        return redirect('viewer')


@apps.route('/editviewer', methods=['POST', 'GET'])
@login_required
def editviewer():
    items = Items.query.order_by(Items.id).all()
    return render_template("editviewer.html", items=items)


@apps.route("/update", methods=["POST", 'GET'])
def update():
    try:
        if request.method == 'POST':
            field = request.form['field']
            value = request.form['value']
            editid = request.form['id']
            print(value, editid, field)
            heh = Items.query.filter_by(id=editid).first()
            print(heh)
            if field == 'name':
                heh.name = value
                print(value)
            if field == 'price':
                heh.price = value
            if field == 'amount':
                heh.amount = value
            db.session.commit()
            success = 1
        return jsonify(success)
    except Exception as e:
        print(e)

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@apps.route('/addtable', methods=['POST', 'GET'])
def addtable():
    if request.method == 'POST':
        route = request.form['route']
        sheetname = request.form['sheetname']
        new_table(rf'{route}', f'{sheetname}')
    return render_template('addtable.html')


@apps.route("/List1")
@login_required
def list1():
    list1 = List1.query.all()
    return render_template("List1.html", List1=list1)


@apps.route('/test', methods=['POST', 'GET'])
@login_required
def test():
    favouriteMoviesForm = FavouriteMoviesForm()
    if favouriteMoviesForm.validate_on_submit():
        print(favouriteMoviesForm.table_name.data)
        cols = []
        for en in favouriteMoviesForm.columns.entries:
            if len(str(en)) > 60:
                print(len(str(en)))
                cols.append(en.data)
        print(cols)
        add_table(favouriteMoviesForm.table_name.data, cols)
        return render_template('test.html', table_name=favouriteMoviesForm.table_name.data, columns=favouriteMoviesForm.columns.entries, form=favouriteMoviesForm)
    return render_template('test.html', form=favouriteMoviesForm)

@apps.route('/HEheHAha', methods=['POST', 'GET'])
@login_required
def HEheHAha():
    if request.method == 'POST':
        type = request.form['type']
        column_x = request.form['column-x']
        column_y = request.form['column-y']
        file_name = request.form['file-name']
        new_chart(file_name, type, column_x, column_y)
    HEheHAha = Hehehaha.query.order_by(Hehehaha.index).all()
    return render_template("HEheHAha.html", HEheHAha=HEheHAha)
    

@apps.route('/adprod_HEheHAha', methods=['POST'])
@login_required
def addprod_HEheHAha():
    if request.method == 'POST':
        col1 = request.form['col1']
        col2 = request.form['col2']
        col3 = request.form['col3']
        
        items = Hehehaha(col1=col1,col2=col2,col3=col3)
        db.session.add(items)
        db.session.commit()
        return redirect('HEheHAha')


@apps.route('/HEheHAha_edit', methods=['POST', 'GET'])
@login_required
def HEheHAha_HEheHAha():
    items = Hehehaha.query.all()
    return render_template("HEheHAha_edit.html", items=items)


@apps.route("/update_HEheHAha", methods=["POST", 'GET'])
def update_HEheHAha():
    try:
        if request.method == 'POST':
            field = request.form['field']
            value = request.form['value']
            editid = request.form['id']
            print(value, editid, field)
            heh = Hehehaha.query.filter_by(index=editid).first()
            print(heh)
            if field == 'username':
                heh.col1 = value
                print(value)
            if field == '2':
                heh.col2 = value
            if field == '3':
                heh.col3 = value
            db.session.commit()
            success = 1
        return jsonify(success)
    except Exception as e:
        print(e)