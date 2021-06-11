from fastapi.testclient import TestClient
import pytest
from os import environ
from psycopg2 import connect
from jwt import decode
from time import time

from main import app


@pytest.fixture()
def client():
    """Prepare application test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def credentials():
    """Prepare valid login credentials."""
    conn = connect(environ['DATABASE_URL'])
    cur = conn.cursor()
    try:
        cur.execute('SELECT name, password FROM users')
        user, password = cur.fetchone()
    finally:
        conn.close()
    return user, password


class TestLogin:
    """Test '/login' endpoint."""
    test_path = '/login'

    def test_auth(self, client, credentials):
        """Test authentication"""
        response_valid = client.get(self.test_path, auth=credentials)
        response_invalid = client.get(self.test_path, auth=('user', 'invalid'))
        response_blank = client.get(self.test_path)

        assert response_valid.status_code == 200
        assert response_invalid.status_code == 401
        assert response_blank.status_code == 401

    def test_token(self, client, credentials):
        """Test received token structure."""
        response = client.get(self.test_path, auth=credentials)
        payload = response.json()

        assert type(payload) is dict
        assert type(payload.get('token')) is str
        token = decode(payload.get('token'), environ['SECRET_KEY'], algorithms=['HS256'])
        assert token.get('name') == credentials[0]
        assert token.get('iat') == round(time())
        assert token.get('exp') == round(time()) + 5 * 60
