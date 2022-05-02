from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


apps = Flask(__name__)
apps.secret_key = 'asdlbwelhbqewglh'
apps.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
apps.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(apps)
manager = LoginManager(apps)

from Httpapp import models, roots

db.create_all()