from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.fixture()
def client():
    """Prepare application test client."""
    with TestClient(app) as test_client:
        yield test_client


def test_categories(client):
    """Test '/categories' endpoint."""
    test_path = '/categories'
    test_record = {'id': 1, 'name': 'Abstract'}

    response = client.get(test_path)
    payload = response.json()

    assert response.status_code == 200
    assert type(payload) is list
    assert test_record in payload
    assert sorted(payload, key=lambda item: item['id']) == payload
