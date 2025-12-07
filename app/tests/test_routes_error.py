import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_error_page(client):
    rv = client.get("/page_not_in_our_project")
    assert rv.status_code == 404