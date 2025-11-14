from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

# find the working directory you are in
basedir =  os.path.abspath(os.path.dirname(__file__))
def create_app():

    myapp_obj = Flask(__name__)
    myapp_obj.config.from_mapping(
        SECRET_KEY = 'you-will-never-guess',
        # appends to working directory app.db
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    db.init_app(myapp_obj)
    with myapp_obj.app_context():
        from . import routes
        db.create_all()

    return myapp_obj
