import os
from app.user import User

CSRF_ENABLED = True
SECRET_KEY = '--SECRET KEY--'

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
UPLOAD_FOLDER = 'static/img/blog/'

ADMINS = [User("admin", "password", 1)]

# Mail Settings
MAIL_SERVER = "smtp.yourmail.com"
MAIL_PORT = "25"
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
DEFAULT_MAIL_SENDER = "SBCA"

basedir = os.path.abspath(os.path.dirname(__file__))
