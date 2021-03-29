import logging
import datetime
from typing import Union, List, Optional

from fastapi import HTTPException, APIRouter, status, Depends
from pydantic import conint

from app import schemas, enums, models, auth
from .depends import get_session, SessionType


logger = logging.getLogger(__name__)


api = APIRouter(tags=['API'])


TYPE_MODEL_MAP = {
    enums.LogType.ohlcv: {'model': models.MarketData, 'schema': schemas.MarketData},
    enums.LogType.kalman: {'model': models.KalmanLogEntry, 'schema': schemas.KalmanLogEntry},
    enums.LogType.bot_performance: {'model': models.BotPerformanceLogEntry, 'schema': schemas.BotPerformanceLogEntry},
    enums.LogType.price_index: {'model': models.PriceIndex, 'schema': schemas.PriceIndex}
}
LogEntity = Union[schemas.BotPerformanceLogEntry, schemas.KalmanLogEntry, schemas.MarketData, schemas.PriceIndex]


@api.post('/log/', response_model=schemas.OkResponse)
def log(
    type: enums.LogType,
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


@api.get('/latest/', response_model=List[LogEntity])
def latest(
    type: enums.LogType,
    exchange: Optional[str] = None,
    symbol: Optional[schemas.symbol_type] = None,
    instrument: Optional[enums.Instrument] = None,
    name: Optional[str] = None,
    bot_id: Optional[int] = None,
    date_end: Optional[datetime.datetime] = None,
    tail: conint(gt=0, lt=35_001) = 1,
    session: SessionType = Depends(get_session),
    user: schemas.UserDB = Depends(auth.get_current_active_user)
) -> List[LogEntity]:
    """
    Returns the latest log data by the specified parameters
    """
    model_class = TYPE_MODEL_MAP[type]['model']
    query = session.query(model_class)
    if type == enums.LogType.ohlcv:
        _locals = locals()
        query = query.filter(
            *[
                getattr(model_class, column_name) == _locals[column_name]
                for column_name in ['exchange', 'symbol', 'instrument']
                if _locals.get(column_name) is not None
            ]
        )
    if type == enums.LogType.price_index and symbol:
        query = query.filter(model_class.symbol == symbol)

    elif type == enums.LogType.kalman and name:
        query = query.filter(model_class.name == name)

    elif type == enums.LogType.bot_performance and bot_id is not None:
        query = query.filter(model_class.bot_id == bot_id)

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
