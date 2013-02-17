import os
from app.user import User

CSRF_ENABLED = True
SECRET_KEY = '--SECRET KEY--'

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

ADMINS = [User("admin", "password", 1)]