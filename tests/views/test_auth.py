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


@pytest.fixture(params=['NO_AUTH', 'WRONG_QUERY_TOKEN', 'WRONG_HEADER_TOKEN'])
def invalid_auth_client(request):
    inv_type = request.param

    def request(method, url):
        method = getattr(client, method)
        if inv_type == 'NO_AUTH':
            return method(url)

        if inv_type == 'WRONG_QUERY_TOKEN':
            return method(f'{url}?api_token=adadas')

        if inv_type == 'WRONG_HEADER_TOKEN':
            return method(url, headers={'Authorization': 'Bearer some'})

    return request


@pytest.mark.parametrize(
    'method, url',
    [
        ('get', '/'),
        ('get', '/openapi.json'),
        ('post', '/log/'),
        ('get', '/latest/')
    ]
)
def test_secure_endpoints(method, url, invalid_auth_client):
    response = invalid_auth_client(method, url)
    assert response.status_code == 401
