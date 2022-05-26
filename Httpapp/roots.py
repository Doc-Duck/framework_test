import flask_login
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList
from wtforms.validators import DataRequired

from Httpapp import db, apps, manager
from Httpapp.models import Items, User, List1 ,Asd #list_add
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
            return redirect(url_for('addprod'))
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
    add_table('asd', ["asfd", "asdf", "ewrg", "dfhg"])
    favouriteMoviesForm = FavouriteMoviesForm()
    if favouriteMoviesForm.validate_on_submit():
        print(favouriteMoviesForm.table_name.data)
        for en in favouriteMoviesForm.columns.entries:
            print(en.data)
        return render_template('test.html', table_name=favouriteMoviesForm.table_name.data, columns=favouriteMoviesForm.columns.entries, form=favouriteMoviesForm)
    return render_template('test.html', form=favouriteMoviesForm)
@apps.route('/asd', methods=['POST', 'GET'])
@login_required
def asd():
    if request.method == 'POST':
        type = request.form['type']
        column_x = request.form['column-x']
        column_y = request.form['column-y']
        file_name = request.form['file-name']
        new_chart(file_name, type, column_x, column_y)
    asd = Asd.query.order_by(Asd.index).all()
    return render_template("asd.html", asd=asd)
    

@apps.route('/adprod_asd', methods=['POST'])
@login_required
def addprod_asd():
    if request.method == 'POST':
        asfd = request.form['asfd']
        asdf = request.form['asdf']
        ewrg = request.form['ewrg']
        dfhg = request.form['dfhg']
        
        items = Asd(asfd=asfd,asdf=asdf,ewrg=ewrg,dfhg=dfhg)
        db.session.add(items)
        db.session.commit()
        return redirect('asd')