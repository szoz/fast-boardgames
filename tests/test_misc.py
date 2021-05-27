from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.fixture()
def client():
    """Prepare application test client."""
    with TestClient(app) as test_client:
        yield test_client


def test_index(client):
    """Test redirect from index endpoint to Open API docs."""
    test_path = '/'

    response = client.get(test_path)

    assert response.status_code == 200
    assert response.url.endswith('/docs')
