import os
from config import basedir
from flask import Flask
from flask_flatpages import FlatPages
from flask.ext.login import LoginManager
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')
pages = FlatPages(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)

from app import views