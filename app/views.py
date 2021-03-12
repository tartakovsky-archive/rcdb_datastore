import logging
from typing import Union, List, Optional

from fastapi import APIRouter, HTTPException

from . import schemas, enums, models
from db.sessions import session

api = APIRouter()
logger = logging.getLogger(__name__)

TYPE_MODEL_MAP = {
    enums.LogType.ohlcv: {'model': models.MarketData, 'schema': schemas.MarketData},
    enums.LogType.kalman: {'model': models.KalmanLogEntry, 'schema': schemas.KalmanLogEntry},
    enums.LogType.bot_performance: {'model': models.BotPerformanceLogEntry, 'schema': schemas.BotPerformanceLogEntry}
}
LogEntity = Union[schemas.BotPerformanceLogEntry, schemas.KalmanLogEntry, schemas.MarketData]


@api.post('/log/', response_model=schemas.OkResponse)
def log(
    type: enums.LogType,
    items: List[LogEntity]
) -> schemas.OkResponse:
    """
    Collects OHLCV data, bot perfomance and kalman logs
    """
    schema_class = TYPE_MODEL_MAP[type]['schema']
    if any(not isinstance(item, schema_class) for item in items):
        raise HTTPException(status_code=422, detail=f"all items should be of '{type.value}' type")

    model_class = TYPE_MODEL_MAP[type]['model']
    session.bulk_save_objects(model_class(**item.dict()) for item in items)
    session.commit()
    return schemas.OkResponse()


@api.get('/latest/', response_model=LogEntity)
def latest(
    type: enums.LogType,
    exchange: Optional[str] = None,
    symbol: Optional[schemas.symbol_type] = None,
    instrument: Optional[enums.Instrument] = None,
    name: Optional[str] = None
) -> LogEntity:
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
    elif name:
        query = query.filter(model_class.name == name)

    instance = query.order_by(model_class.timestamp.desc()).limit(1).first()
    if not instance:
        raise HTTPException(
            status_code=404,
            detail=f'Entity {type} with the specified parameters not found'
        )

    return TYPE_MODEL_MAP[type]['schema'](**instance.to_dict(exclude=['id']))
