import pytest

def test_home(client): # make sure you have all modules used in the code downloaded
    rv = client.get("/", follow_redirects=True)
    assert rv.status_code == 200
    assert b"Sign In" in rv.data

def test_error_page(client):
    rv = client.get("/page_not_in_our_project")
    assert rv.status_code == 404

def test_login(client):
    rv = client.get("/auth/login")
    assert rv.status_code == 200
    assert b"Sign In" in rv.data

def test_redirect(client):
    rv = client.get("/redirect")
    assert rv.status_code == 302
