import asyncio
import time
from datetime import datetime
from importlib import resources

import orjson
import pytest
from rcdb_commons.lib.stores import DataType

from app.views.log import TYPE_MODEL_MAP
from app.views.depends import get_redis


VALID_ITEMS = orjson.loads(resources.read_text('tests.datasets', 'valid_log_data.json'))


@pytest.mark.parametrize('payload_type, items', VALID_ITEMS)
def test_log(payload_type, items, auth_client, drop_tables, session):
    response = auth_client.post(f'/log/?type={payload_type}', json=items)
    assert response.status_code == 200, response.text

    data = [
        orjson.loads(orjson.dumps(inst.to_dict(exclude=['id'])))
        for inst in session.query(TYPE_MODEL_MAP[DataType[payload_type]]['model']).all()
    ]

    assert all(inst_data in items for inst_data in data)


@pytest.mark.parametrize('payload_type, items', VALID_ITEMS)
def test_log_ts(payload_type, items, auth_client, drop_tables, session):
    now = time.time()
    items = [{**item, 'timestamp': now + i} for i, item in enumerate(items)]
    response = auth_client.post(f'/log/?type={payload_type}', json=items)
    assert response.status_code == 200, response.text

    timestamps = {datetime.utcfromtimestamp(item['timestamp']) for item in items}
    assert all([
        inst.timestamp in timestamps
        for inst in session.query(TYPE_MODEL_MAP[DataType[payload_type]]['model']).all()
    ])


@pytest.mark.parametrize(
    'payload_type, items',
    orjson.loads(resources.read_text('tests.datasets', 'invalid_log_data.json'))
)
def test_log_invalid_schema(payload_type, items, auth_client):
    response = auth_client.post(f'/log/?type={payload_type}', json=items)
    assert response.status_code == 422


@pytest.fixture(
    params=(
        (query_item, valid_items)
        for query_items, valid_items in zip(
            orjson.loads(resources.read_text('tests.datasets', 'query_params_for_latest.json')),
            VALID_ITEMS
        )
        for query_item in query_items
    )
)
def latest_valid_data(request, drop_tables, session):
    query_param, valid_items = request.param
    type = DataType[valid_items[0]]
    model_class = TYPE_MODEL_MAP[type]['model']
    schema_class = TYPE_MODEL_MAP[type]['schema']
    session.bulk_save_objects(
        model_class(**schema_class(**item).dict())
        for item in valid_items[1]
    )
    session.commit()
    yield query_param['params'], valid_items[1][query_param['index']], valid_items


def test_latest(latest_valid_data, auth_client):
    query_params, test_response_data, _ = latest_valid_data
    response = auth_client.get(f'/latest/{query_params}')
    assert response.json()[0] == test_response_data


@pytest.mark.parametrize(
    'payload_type, items',
    orjson.loads(resources.read_text('tests.datasets', 'lowercase_log_data.json'))
)
def test_lowercase_data_log(payload_type, items, auth_client, drop_tables):
    response = auth_client.post(f'/log/?type={payload_type}', json=[items[0]])
    assert response.status_code == 200, response.text

    response = auth_client.get(f'/latest/?type={payload_type}')
    assert response.json()[0] == items[1]


def test_latest_tail(latest_valid_data, auth_client):
    tail = 2
    *_, valid_items = latest_valid_data
    query_type, valid_items = valid_items

    valid_items = tuple(sorted(valid_items, key=lambda x: x['timestamp'], reverse=True)[:tail])

    response = auth_client.get(f'/latest/?type={query_type}&tail={tail}')
    assert tuple(response.json()) == valid_items


@pytest.fixture(
    params=(
        (query_item, valid_items)
        for query_item, valid_items in zip(
            orjson.loads(resources.read_text('tests.datasets', 'query_params_date_end.json')),
            VALID_ITEMS
        )
    )
)
def date_end_valid_data(request, drop_tables, session):
    query_item, valid_items = request.param
    type = DataType[valid_items[0]]
    model_class = TYPE_MODEL_MAP[type]['model']
    schema_class = TYPE_MODEL_MAP[type]['schema']
    session.bulk_save_objects(
        model_class(**schema_class(**item).dict())
        for item in valid_items[1]
    )
    session.commit()

    yield query_item['params'], tuple(valid_items[1])[slice(*query_item['slice'])] if query_item['slice'] else tuple()


def test_latest_date_end(date_end_valid_data, auth_client):
    params, valid_items = date_end_valid_data
    response = auth_client.get(f'/latest/{params}')
    if not valid_items:
        assert response.status_code == 404
    else:
        assert tuple(response.json()) == tuple(sorted(valid_items, key=lambda r: r['timestamp'], reverse=True))


@pytest.mark.parametrize('tail', (-1, 0, 35_001))
def test_latest_tail_constraint(tail, auth_client):
    response = auth_client.get(f'/latest/?type=ohlcv&tail={tail}')
    msg = response.json()['detail'][0]['msg']

    assert response.status_code == 422
    assert 'ensure this value is less than 35001' == msg or 'ensure this value is greater than 0' == msg


@pytest.fixture
def fill_db_valid_data(drop_tables, session):
    for valid_items in VALID_ITEMS:
        type = DataType[valid_items[0]]
        model_class = TYPE_MODEL_MAP[type]['model']
        schema_class = TYPE_MODEL_MAP[type]['schema']
        session.bulk_save_objects(
            model_class(**schema_class(**item).dict())
            for item in valid_items[1]
        )
    session.commit()
    yield


@pytest.mark.parametrize(
    'query_params, result',
    [
        (
            'type=ohlcv',
            {
                "timestamp": "2021-03-10T12:15:57.393693",
                "exchange": "FOREX",
                "symbol": "BTC/USDT",
                "instrument": "SPOT",
                "open": 54953.05,
                "high": 54963.05,
                "low": 54933.05,
                "close": 54965.05,
                "volume": 1231254953.05
            }
        ),
        (
            'type=kalman&name=name2&field=s1_x',
            0.35
        ),
        (
            'type=bot_performance&field=price_fair',
            12245.45
        ),
        (
            'type=price_index&symbol=EUR/USDT&field=price',
            1.17117149
        ),
        (
            'type=account_trades&name=et_bn_sub10&field=price_avg_buy',
            5
        ),
        (
            'type=account_trades&account_type=SPOT&field=price_avg_sell',
            3.7
        ),
        (
            'type=rebates&field=rebate',
            13.5
        ),
    ]
)
def test_latest_value(query_params, result, auth_client, fill_db_valid_data):
    response = auth_client.get(f'/latest-value/?{query_params}')
    assert response.json() == result


FOREX_PRICES = [
    {'timestamp': 1622182669, 'symbol': 'SGD/TRY', 'ask': 6.454495, 'bid': 6.454015},
    {'timestamp': 1622182669, 'symbol': 'EUR/AUD', 'ask': 1.57734, 'bid': 1.57727}
]


@pytest.fixture(scope='module')
def fill_forex_prices():
    async def _():
        redis = [r async for r in get_redis()][0]
        for price in FOREX_PRICES:
            await redis.hmset_dict(f'fx:{price["symbol"]}', price)

        redis.close()
        await redis.wait_closed()
    asyncio.run(_())


def test_price(fill_forex_prices, auth_client):
    response = auth_client.get('/prices/?symbol=SGD%2FTRY&symbol=EUR%2FAUD&symbol=EUR%2FUSDT')
    assert tuple(response.json()) == tuple(FOREX_PRICES)
