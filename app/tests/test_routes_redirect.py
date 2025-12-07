import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_redirect(client):
    rv = client.get("/redirect")
    assert rv.status_code == 302

