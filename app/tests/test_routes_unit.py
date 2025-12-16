from werkzeug.security import generate_password_hash
from app.models import Student
from app import g_DB as db
from flask import get_flashed_messages
import pytest

#empty route should redirect users to auth/login page
def test_home(client):
    rv = client.get("/", follow_redirects=True)
    assert rv.status_code == 200
    assert b"Sign In" in rv.data

#non-existent route should return PAGE NOT FOUND (404)
def test_error_page(client):
    rv = client.get("/page_not_in_our_project")
    assert rv.status_code == 404

#login page should display Sign In
def test_login(client):
    rv = client.get("/auth/login")
    assert rv.status_code == 200
    assert b"Sign In" in rv.data

#redirects should give a 302 status code
def test_redirect(client):
    rv = client.get("/redirect")
    assert rv.status_code == 302


## A succesful log-in means 200 (success) status code, one redirect (len == 1), and a flashed "Login Succesful" ##
def test_user_login_good(client):
    #fixture starts with empty DB so lets just create a user and add it to DB
    hashed_pass = generate_password_hash("ILikeTurtles")
    user = Student(username="JohnDoe", password=hashed_pass, email="john@sample.com")
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    #post the data
    rv = client.post('/auth/login', data={
        'username': 'JohnDoe',
        'password': 'ILikeTurtles'
    }, follow_redirects=True)

    #verify redirection and content
    assert rv.status_code == 200
    assert len(rv.history) == 1
    assert b"Login Successful" in rv.data  #b means byte-string


## A missing user should still generate a succesful site, redirected to try again, and flash a "No user..." message ##
def test_user_login_user_missing(client):
    #fixture starts with empty DB so lets just create a user and add it to DB
    hashed_pass = generate_password_hash("ILikeTurtles")
    user = Student(username="JohnDoe", password=hashed_pass, email="john@sample.com")
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    #post the data
    rv = client.post('/auth/login', data={
        'username': 'JaneDoe',
        'password': 'ILikeTurtles'
    }, follow_redirects=False)

    #verify redirection and content
    assert rv.status_code == 302
    assert rv.location.endswith('/auth/login')
    with client.session_transaction() as sess:
        flashes = sess.get('_flashes', [])
        assert any("No user named 'JaneDoe'" in f[1] for f in flashes)

## A wrong password should redirect to the same page, and also flash a "Wrong..." message
def test_user_login_bad_password(client):
    #fixture starts with empty DB so lets just create a user and add it to DB
    hashed_pass = generate_password_hash("ILikeTurtles")
    user = Student(username="JohnDoe", password=hashed_pass, email="john@sample.com")
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    #post the data
    rv = client.post('/auth/login', data={
        'username': 'JohnDoe',
        'password': 'ILikeTrains'
    }, follow_redirects=True)

    #verify redirection and content
    assert rv.status_code == 200
    assert len(rv.history) == 1
    assert b"Wrong password, try again." in rv.data
