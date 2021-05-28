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


class TestBoardgames:
    """Test '/boardgames' endpoint."""
    test_path = '/boardgames'

    def test_basic(self, client):
        """Test basic response parameters."""
        response = client.get(self.test_path)
        payload = response.json()

        assert response.status_code == 200
        assert type(payload) is list
        assert type(payload[0]) is dict

    def test_pagination(self, client):
        """Test response pagination"""
        params_invalid = [{'limit': 0}, {'limit': -1}, {'page': 0}, {'page': -1}]
        params_valid = [{}, {'limit': 10}, {'limit': 10, 'page': 2}]

        responses_invalid = [client.get(self.test_path, params=params) for params in params_invalid]
        responses_valid = [client.get(self.test_path, params=params) for params in params_valid]
        payloads = [response.json() for response in responses_valid]

        for response in responses_invalid:
            assert response.status_code == 422
        for response in responses_valid:
            assert response.status_code == 200
        assert len(payloads[0]) == 20
        assert len(payloads[1]) == 10
        assert len(payloads[2]) == 10
        assert payloads[0] == payloads[1] + payloads[2]
