from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

apps = Flask(__name__)
apps.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
apps.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(apps)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(100), nullable=False)

    def __repr__(self):
        return '<Items %r>' % self.id


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Float(100), nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id


@apps.route('/')
def index():
    return render_template('index.html')


@apps.route('/admin')
def admin():
    return render_template('admin.html')


@apps.route('/adprod', methods=['POST', 'GET'])
def adduser():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        items = Items(name=name, price=price)
        print(price)
        db.session.add(items)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('adprod.html')


@apps.route('/viewer')
def viewer():
    items = Items.query.order_by(Items.id).all()
    return render_template("viewer.html", items=items)


if __name__ == '__main__':
    apps.run(debug=True, use_reloader=False)
