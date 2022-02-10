import logging
import datetime
import operator
from typing import Union, List, Optional, Callable

import aioredis
from fastapi import HTTPException, APIRouter, status, Depends, Query
from pydantic import conint, BaseModel, Field, validator
from rcdb_commons.lib.stores import DataType
from rcdb_commons.lib.schemas.exchange import AccountType, TransferType

from app import schemas, enums, models, auth
from .depends import get_session, get_redis, SessionType


logger = logging.getLogger(__name__)


api = APIRouter(tags=['API'])


class FilterColumn(BaseModel):
    """
    Column filter:
        session.query(Entity).filter(
            fc.matching_expression_func(
                getattr(Entity, fc.field_name),
                fc.transform_func(GET_QUERY_PARAMETERS[fc.query_param_name])
            )
        )
    """
    field_name: str
    query_param_name: str
    transform_func: Callable = Field(default=lambda query_param_value: query_param_value)
    matching_expression_func: Callable = Field(default=lambda field, value: field == value)

    def __init__(self, *args, **kwargs):
        if args and not isinstance(args[0], dict):
            for k, v in zip(
                ['field_name', 'query_name', 'transform_func', 'matching_expression_func'][:len(args)],
                args
            ):
                kwargs[k] = v
            args = []
            if not kwargs.get('query_param_name'):
                kwargs['query_param_name'] = kwargs.get('field_name')
        super().__init__(*args, **kwargs)

    @validator('query_param_name', pre=True, always=True)
    def default_query_param_name(cls, v, *, values, **kwargs):
        return v or values['field_name']


ACCOUNT_TYPE_FILTER = FilterColumn('account_type', transform_func=operator.attrgetter('value'))


TYPE_MODEL_MAP = {
    DataType.ohlcv: {
        'model': models.MarketData,
        'schema': schemas.MarketData,
        'filter_columns': ['exchange', 'symbol', 'instrument', ACCOUNT_TYPE_FILTER]
    },
    DataType.kalman: {
        'model': models.KalmanLogEntry,
        'schema': schemas.KalmanLogEntry,
        'filter_columns': ['name', FilterColumn('name', 'symbol')]
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
    },
    DataType.balance: {
        'model': models.Balance,
        'schema': schemas.Balance,
        'filter_columns': ['name', 'symbol', ACCOUNT_TYPE_FILTER]
    },
    DataType.transfers: {
        'model': models.Transfer,
        'schema': schemas.Transfer,
        'filter_columns': [
            'name',
            'symbol',
            'is_sub_account_transfer',
            FilterColumn(
                'transfer_type',
                transform_func=lambda x: list(map(operator.attrgetter('value'), x)),
                matching_expression_func=(
                    lambda field, value: field.in_(value)
                )
            )
        ]
    },
    DataType.bswap_quote: {
        'model': models.BSwapQuote,
        'schema': schemas.BSwapQuote,
        'filter_columns': ['symbol']
    },
    DataType.orderbook: {
        'model': models.Orderbook,
        'schema': schemas.Orderbook,
        'filter_columns': ['channel']
    },
    DataType.kalman_log: {
        'model': models.KalmanLog,
        'schema': schemas.KalmanLog,
        'filter_columns': ['channel']
    },
    DataType.trades_log: {
        'model': models.TradeLog,
        'schema': schemas.TradeLog,
        'filter_columns': ['channel']
    },
    DataType.tickers: {
        'model': models.Ticker,
        'schema': schemas.Ticker,
        'filter_columns': ['channel']
    }
}
LogEntity = Union[
    schemas.AccountTrade,
    schemas.Balance,
    schemas.BidAsk,
    schemas.BotPerformanceLogEntry,
    schemas.BSwapQuote,
    schemas.KalmanLogEntry,
    schemas.KalmanLog,
    schemas.MarketData,
    schemas.Orderbook,
    schemas.PriceIndex,
    schemas.Rebate,
    schemas.Ticker,
    schemas.Transfer,
    schemas.TradeLog
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


def get_filters(columns: List[Union[str, FilterColumn]], _locals, model_class):
    return [
        filter_column.matching_expression_func(
            getattr(model_class, filter_column.field_name),
            filter_column.transform_func(_locals[filter_column.query_param_name])
        )
        for filter_column in map(
            lambda x: FilterColumn(x) if isinstance(x, str) else x,
            columns
        )
        if _locals.get(filter_column.query_param_name) is not None
    ]


@api.get('/latest/', response_model=Union[List[LogEntity], Optional[Union[str, int, float]]])
def latest(
    type: DataType,
    exchange: Optional[str] = None,
    symbol: Optional[schemas.symbol_type] = None,
    instrument: Optional[enums.Instrument] = None,
    account_type: Optional[AccountType] = None,
    channel: Optional[str] = None,
    transfer_type: Optional[List[TransferType]] = Query(None),
    name: Optional[str] = None,
    bot_id: Optional[int] = None,
    date_start: Optional[datetime.datetime] = None,
    date_end: Optional[datetime.datetime] = None,
    is_sub_account_transfer: Optional[bool] = None,
    field: Optional[str] = None,
    tail: conint(gt=0, lt=100_001) = 1,
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

    if date_start:
        query = query.filter(model_class.timestamp >= date_start)

    if date_end:
        query = query.filter(model_class.timestamp < date_end)

    if model_class == models.Rebate:
        order = model_class.timestamp_received.desc()
    else:
        order = model_class.timestamp.desc()

    instances = query.order_by(order).limit(tail).all()
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
    channel: Optional[str] = None,
    transfer_type: Optional[List[TransferType]] = Query(None),
    name: Optional[str] = None,
    bot_id: Optional[int] = None,
    is_sub_account_transfer: Optional[bool] = None,
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
        channel=channel,
        name=name,
        bot_id=bot_id,
        session=session,
        user=user,
        transfer_type=transfer_type,
        is_sub_account_transfer=is_sub_account_transfer
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
    for sym in (symbol or []):
        pipe.hgetall(f'{prefix}:{sym}', encoding='utf-8')

    return list(filter(bool, await pipe.execute()))
