from flask_sqlalchemy import SQLAlchemy
g_DB = SQLAlchemy()

from flask import Flask, render_template
from .config import create_app_config
from .session import session_get_current_user_dict
import os


def create_app():
    myapp_obj = Flask(__name__)
    create_app_config(myapp_obj);

    g_DB.init_app(myapp_obj)

    if not os.path.exists(myapp_obj.config['UPLOADS']):
        os.makedirs(myapp_obj.config['UPLOADS'])
    if not os.path.exists(myapp_obj.config['RESOURCES']):
        os.makedirs(myapp_obj.config['RESOURCES'])

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

def db_commit():
    g_DB.session.commit();

'''NOTE:(khanh): MUST CALL THIS INSTEAD OF render_template!!!!!
    Because I passed in a UserData object into the base html. This enables the dropdown menu to work
    Pass arguments like how you pass arguments to render_template
'''
def app_render_template(file_name, *args, **kw_args):
    return render_template(file_name, *args, **kw_args, userdata=session_get_current_user_dict())
