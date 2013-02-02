#!venv/bin/python
from app import app
from app.config import DEBUG 
app.run(host='0.0.0.0', debug = DEBUG)