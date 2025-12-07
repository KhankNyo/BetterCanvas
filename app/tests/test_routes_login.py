import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_login(client):
    rv = client.get("/auth/login")
    assert rv.status_code == 200
    assert b"Sign In" in rv.data