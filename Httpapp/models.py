from flask_login import UserMixin

from Httpapp import db, manager


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(100), nullable=False)
    amount = db.Column()

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


class List1(db.Model):
	index = db.Column(primary_key=True)
	Unnamed0 = db.Column()
	BazaTMTs = db.Column()
	Tip = db.Column()
	Razmer = db.Column()
	Bazapokupatelja = db.Column()
	Tip1 = db.Column()
	Razmer1 = db.Column()
	Baza4postavschik = db.Column()
	Unnamed8 = db.Column()
	Unnamed9 = db.Column()
	Sdelka = db.Column()
	Unnamed11 = db.Column()


