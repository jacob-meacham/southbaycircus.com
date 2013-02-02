import os
from config import basedir
from flask import Flask
from flask_flatpages import FlatPages

app = Flask(__name__)
app.config.from_object('config')
pages = FlatPages(app)

from app import views