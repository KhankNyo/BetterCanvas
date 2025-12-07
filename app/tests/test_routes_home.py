import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_home(client): # make sure you have all modules used in the code downloaded
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Welcome to Simpler Canvas!" in rv.data










