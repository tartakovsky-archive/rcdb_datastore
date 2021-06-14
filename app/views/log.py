import logging
import datetime
import operator
from typing import Union, List, Optional

import aioredis
from fastapi import HTTPException, APIRouter, status, Depends, Query
from pydantic import conint
from rcdb_commons.lib.stores import DataType
from rcdb_commons.lib.schemas.exchange import AccountType

from app import schemas, enums, models, auth
from .depends import get_session, get_redis, SessionType


logger = logging.getLogger(__name__)


api = APIRouter(tags=['API'])

ACCOUNT_TYPE_FILTER = ('account_type', 'account_type', operator.attrgetter('value'))
TYPE_MODEL_MAP = {
    DataType.ohlcv: {
        'model': models.MarketData,
        'schema': schemas.MarketData,
        'filter_columns': ['exchange', 'symbol', 'instrument', ACCOUNT_TYPE_FILTER]
    },
    DataType.kalman: {
        'model': models.KalmanLogEntry,
        'schema': schemas.KalmanLogEntry,
        'filter_columns': ['name', ('name', 'symbol')]
    },
    DataType.bot_performance: {
        'model': models.BotPerformanceLogEntry,
        'schema': schemas.BotPerformanceLogEntry,
        'filter_columns': ['bot_id']
    },
    DataType.price_index: {
        'model': models.PriceIndex,
        'schema': schemas.PriceIndex,
        'filter_columns': ['symbol']
    },
    DataType.account_trades: {
        'model': models.AccountTrade,
        'schema': schemas.AccountTrade,
        'filter_columns': ['name', 'symbol', ACCOUNT_TYPE_FILTER]
    },
    DataType.rebates: {
        'model': models.Rebate,
        'schema': schemas.Rebate,
        'filter_columns': ['name', 'symbol', ACCOUNT_TYPE_FILTER]
    },
    DataType.bid_ask: {
        'model': models.BidAsk,
        'schema': schemas.BidAsk,
        'filter_columns': ['exchange', 'symbol', ACCOUNT_TYPE_FILTER]
    }
}
LogEntity = Union[
    schemas.AccountTrade,
    schemas.BidAsk,
    schemas.BotPerformanceLogEntry,
    schemas.KalmanLogEntry,
    schemas.MarketData,
    schemas.PriceIndex,
    schemas.Rebate
]


@api.post('/log/', response_model=schemas.OkResponse)
def log(
    type: DataType,
    items: List[LogEntity],
    session: SessionType = Depends(get_session),
    user: schemas.UserDB = Depends(auth.get_current_active_user)
) -> schemas.OkResponse:
    """
    Collects OHLCV data, binance price index, bot performance and kalman logs
    """
    schema_class = TYPE_MODEL_MAP[type]['schema']
    if any(not isinstance(item, schema_class) for item in items):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"all items should be of '{type.value}' type"
        )

    model_class = TYPE_MODEL_MAP[type]['model']
    session.bulk_save_objects(model_class(**item.dict()) for item in items)
    session.commit()
    return schemas.OkResponse()


def get_filters(columns, _locals, model_class):
    def transform(x):
        return x

    # transform columns to form (db field name, incoming data field name, transform func)
    columns = [
        (
            c if len(c) == 3 else (*c, transform)
        ) if isinstance(c, tuple) else (
            (c, c, transform)
        )
        for c in columns
    ]
    return [
        getattr(model_class, field_name) == transform_func(_locals[param_key])
        for field_name, param_key, transform_func in columns
        if _locals.get(param_key) is not None
    ]


@api.get('/latest/', response_model=Union[List[LogEntity], Optional[Union[str, int, float]]])
def latest(
    type: DataType,
    exchange: Optional[str] = None,
    symbol: Optional[schemas.symbol_type] = None,
    instrument: Optional[enums.Instrument] = None,
    account_type: Optional[AccountType] = None,
    name: Optional[str] = None,
    bot_id: Optional[int] = None,
    date_end: Optional[datetime.datetime] = None,
    field: Optional[str] = None,
    tail: conint(gt=0, lt=35_001) = 1,
    session: SessionType = Depends(get_session),
    user: schemas.UserDB = Depends(auth.get_current_active_user)
) -> List[LogEntity]:
    """
    Returns the latest log data by the specified parameters
    """
    model_class = TYPE_MODEL_MAP[type]['model']
    query = session.query(model_class).filter(
        *get_filters(
            TYPE_MODEL_MAP[type]['filter_columns'],
            model_class=model_class,
            _locals=locals()
        )
    )

    if date_end:
        query = query.filter(model_class.timestamp < date_end)

    instances = query.order_by(model_class.timestamp.desc()).limit(tail).all()
    if not instances:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Entity {type} with the specified parameters not found'
        )

    return [
        TYPE_MODEL_MAP[type]['schema'](**instance.to_dict(exclude=['id']))
        for instance in instances
    ]


@api.get('/latest-value/', response_model=Union[LogEntity, float, str, datetime.datetime, None])
def latest_value(
    type: DataType,
    exchange: Optional[str] = None,
    symbol: Optional[schemas.symbol_type] = None,
    instrument: Optional[enums.Instrument] = None,
    account_type: Optional[AccountType] = None,
    name: Optional[str] = None,
    bot_id: Optional[int] = None,
    field: Optional[str] = None,
    session: SessionType = Depends(get_session),
    user: schemas.UserDB = Depends(auth.get_current_active_user)
) -> Union[LogEntity, float, str, datetime.datetime, None]:
    """
    Same as /latest/, but can return a specified field
    """
    if field and field not in TYPE_MODEL_MAP[type]['schema'].__fields__:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Entity {type} does not have field `{field}`'
        )

    response_data = latest(
        type=type,
        exchange=exchange,
        symbol=symbol,
        instrument=instrument,
        account_type=account_type,
        name=name,
        bot_id=bot_id,
        session=session,
        user=user
    )

    response_data = response_data[0]
    if field:
        return getattr(response_data, field)
    return response_data


@api.get('/prices/', response_model=List[schemas.ForexPrice])
async def prices(
    symbol: List[str] = Query(None),
    redis: aioredis.Redis = Depends(get_redis),
    user: schemas.UserDB = Depends(auth.get_current_active_user)
):
    """
    Returns latest forex prices
    """
    prefix = 'fx'
    pipe = redis.pipeline()
    for sym in symbol:
        pipe.hgetall(f'{prefix}:{sym}', encoding='utf-8')

    return list(filter(bool, await pipe.execute()))
