import pytest

from db.sessions import session
from app.models import MODELS


@pytest.fixture
def drop_tables():
    yield
    for model in MODELS:
        session.query(model).delete()
    session.commit()
