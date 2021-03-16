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


@pytest.fixture
def auth_client(user):
    client = TestClient(app)
    client.headers.update({'Authorization': f'Bearer {auth.encode_token(user)}'})
    yield client
