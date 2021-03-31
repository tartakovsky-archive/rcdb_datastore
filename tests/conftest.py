import pytest
from fastapi.testclient import TestClient

from app import auth, app
from app.views.depends import get_session
from app.models import MODELS


USER = {
    'username': 'admin',
    'password': 'password'
}


@pytest.fixture
def drop_tables(session):
    yield
    for model in MODELS:
        session.query(model).delete()
    session.commit()


@pytest.fixture(scope='session')
def session():
    yield from get_session()


@pytest.fixture
def user(drop_tables, session):
    yield auth.create_user(**USER, session=session)


@pytest.fixture(params=['AUTH-HEADER', 'AUTH-QUERY-PARAMETER'])
def auth_client(user, request):
    client = TestClient(app)
    token = auth.encode_token(user)

    if request.param == 'AUTH-HEADER':
        client.headers.update({'Authorization': f'Bearer {token}'})
        yield client
    else:

        class _client:
            def auth_url(self, url):
                api_key_param = f'api_token={token}'
                if '?' in url:
                    url += f'&{api_key_param}'
                else:
                    url += f'?{api_key_param}'
                return url

            def get(self, url, **kwargs):
                return client.get(self.auth_url(url), **kwargs)

            def post(self, url, **kwargs):
                return client.post(self.auth_url(url), **kwargs)

        yield _client()
