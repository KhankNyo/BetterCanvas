import pytest, unittest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

#for some reason, these work individually but when the whole file is run, it causes a 404 error
def test_home(client): # make sure you have all modules used in the code downloaded
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Welcome to Simpler Canvas!" in rv.data

def test_login(client):
    rv = client.get("/auth/login")
    assert rv.status_code == 200
    assert b"Sign In" in rv.data

def test_redirect(client):
    rv = client.get("/redirect")
    assert rv.status_code == 302











