import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)

from app import routes
