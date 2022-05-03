from flask_login import UserMixin

from Httpapp import db, manager


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(100), nullable=False)

    def __repr__(self):
        return "%s %s" % (str(self.name), str(self.price))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column
    role = db.Column(db.Float(100), nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False,)
    is_Admin = db.Column(db.Boolean, default=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

