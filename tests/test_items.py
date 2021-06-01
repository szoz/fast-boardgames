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
    categories_path = '/categories'
    display_keys = ['score', 'complexity', 'name']

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

    @pytest.mark.parametrize('key', display_keys)
    def test_sorting(self, client, key, extra_params=None):
        """Test response sorting"""
        if extra_params is None:
            extra_params = {}
        response_asc = client.get(self.test_path, params={'sort': key, 'limit': 100, **extra_params})
        response_desc = client.get(self.test_path, params={'sort': f'-{key}', 'limit': 100, **extra_params})
        payload_asc = [{key: value for key, value in record.items()
                        if key in self.display_keys}
                       for record in response_asc.json()]
        payload_desc = [{key: value for key, value in record.items()
                         if key in self.display_keys}
                        for record in response_desc.json()]

        assert sorted(payload_asc, key=lambda item: item[key]) == payload_asc
        assert sorted(payload_desc, key=lambda item: item[key], reverse=True) == payload_desc

    def test_filter_complexity(self, client):
        """Test response filter by complexity level."""
        filter_values = {'simple': [1, 2], 'easy': [2, 3], 'medium': [3, 4], 'hard': [4, 5]}

        responses = [client.get(self.test_path, params={'complexity': value}) for value in filter_values]
        payloads = [response.json() for response in responses]

        for payload, (minimum, maximum) in zip(payloads, filter_values.values()):
            assert all(minimum <= record['complexity'] < maximum
                       for record in payload)

    def test_filter_category(self, client):
        """Test response filter by category"""
        all_categories = [record['name'] for record in client.get(self.categories_path).json()]
        cased_categories = [all_categories[0], all_categories[1].upper(), all_categories[2].lower()]
        responses = [client.get(self.test_path, params={'category': category}) for category in cased_categories]
        payloads = [response.json() for response in responses]

        for payload, category in zip(payloads, all_categories[:3]):
            assert all(category in [element['name'] for element in record['categories']]
                       for record in payload)

    def test_filter_sort(self, client):
        """Test sorting in response filtered by category"""
        category = client.get(self.categories_path).json()[0]['name']

        response_asc = client.get(self.test_path, params={'sort': 'name', 'category': category})
        response_desc = client.get(self.test_path, params={'sort': '-name', 'category': category})
        payloads_asc = [{key: value for key, value in record.items()
                         if key in self.display_keys}
                        for record in response_asc.json()]
        payloads_desc = [{key: value for key, value in record.items()
                          if key in self.display_keys}
                         for record in response_desc.json()]

        assert sorted(payloads_asc, key=lambda item: item['name']) == payloads_asc
        assert sorted(payloads_desc, key=lambda item: item['name'], reverse=True) == payloads_desc


def test_boardgame(client):
    """Test '/boardgames/{id}' endpoint."""
    test_path = '/boardgames/{id}'
    test_id = 5
    invalid_ids = [-2, 0, 999]

    responses_invalid = [client.get(test_path.format(id=invalid_id)) for invalid_id in invalid_ids]
    response_valid = client.get(test_path.format(id=test_id))

    for response in responses_invalid:
        assert response.status_code in [404, 422]
    assert response_valid.status_code == 200
    assert type(response_valid.json()) is dict
    assert response_valid.json()['id'] == test_id
