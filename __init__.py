import os
from config import basedir, MAIL_SERVER, MAIL_PORT, DEFAULT_MAIL_SENDER, MAIL_USERNAME, MAIL_PASSWORD, ADMINS
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

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), DEFAULT_MAIL_SENDER, ADMINS, 'SBCA.com Failure!', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/sbca.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('sbca startup')

from app import views