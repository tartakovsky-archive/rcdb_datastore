import pytest
from fastapi.testclient import TestClient

from app import app, auth
from tests.conftest import USER


client = TestClient(app)


def test_login(user, session):
    response = client.post('/token/', data=USER)
    auth_data = response.json()
    assert auth.decode_token(auth_data['access_token'], session=session) == user
    assert auth_data['token_type'] == 'bearer'


@pytest.mark.parametrize(
    'method, url',
    [
        ('get', '/'),
        ('get', '/openapi.json'),
        ('post', '/log/'),
        ('get', '/latest/')
    ]
)
def test_secure_endpoints(method, url):
    response = getattr(client, method)(url)
    assert response.status_code == 401
