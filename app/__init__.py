from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import create_app_config

g_DB = SQLAlchemy()

def create_app():

    myapp_obj = Flask(__name__)
    create_app_config(myapp_obj);

    g_DB.init_app(myapp_obj)
    with myapp_obj.app_context():
        from .auth import routes
        from .main import routes
        g_DB.create_all()

    return myapp_obj

'''Add something to the db and commit'''
def db_add_now(thing):
    g_DB.session.add(thing);
    g_DB.session.commit();

'''Delete something to the db and commit'''
def db_delete_now(thing):
    g_DB.session.delete(thing);
    g_DB.session.commit();

