import pytest
from app import create_app, g_DB as db

@pytest.fixture(autouse=True)
def client():
    app = create_app()
    #this will force the tests to use a clean, empty DB for EVERY test
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CRSF_ENABLED'] = False

    with app.app_context():
        ## SETUP ##
        db.create_all() #create the database from the given models - EMPTY
        with app.test_client() as client:
            yield client  ## TEST ##
        ## TEARDOWN ##
        db.session.rollback()
        db.session.remove()
        db.drop_all() #drop all records from the database just in case
