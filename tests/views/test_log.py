import orjson

import pytest
from importlib import resources
from fastapi.testclient import TestClient

from app import app
from app.enums import LogType
from app.views import TYPE_MODEL_MAP
from db.sessions import session

client = TestClient(app)


@pytest.mark.parametrize(
    'payload_type, items',
    orjson.loads(resources.read_text('tests.datasets', 'valid_log_data.json'))
)
def test_log(payload_type, items, drop_tables):
    response = client.post(f'/log/?payload_type={payload_type}', json=items)
    assert response.status_code == 200, response.text

    data = [
        orjson.loads(orjson.dumps(inst.to_dict(exclude=['id'])))
        for inst in session.query(TYPE_MODEL_MAP[getattr(LogType, payload_type)]['model']).all()
    ]

    assert all(inst_data in items for inst_data in data)
