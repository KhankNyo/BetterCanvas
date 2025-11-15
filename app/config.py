import os

# NOTE: the basedir is that of this file, so the db will be where config.py is
g_BASE_DIR =  os.path.abspath(os.path.dirname(__file__))

# appends to working directory app.db
g_DATABASE_PATH = 'sqlite:///' + os.path.join(g_BASE_DIR, 'app.db')

def create_app_config(myapp_obj):
    myapp_obj.config.from_mapping(
        SECRET_KEY = 'you-will-never-guess',
        SQLALCHEMY_DATABASE_URI = g_DATABASE_PATH,
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )


