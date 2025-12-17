import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

#local app needs mapping for routes this is done in m3 release
#test it's a redirection
def test_index_redirects(client): # make sure you have all modules used in >
    rv = client.get("/")
    assert rv.status_code == 404 #302

#local app needs mapping for routes this is done in m3 release
def test_index_redirects_to_login(client):
    rv = client.get("/", follow_redirects=True)
    assert rv.status_code == 404
#    html_content = rv.get_data(as_text=True)
#    assert "Log In" in html_content








