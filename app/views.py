from typing import Union, List
from fastapi import APIRouter, HTTPException

from . import schemas, enums, models
from db.sessions import session

api = APIRouter()

TYPE_MODEL_MAP = {
    enums.LogType.ohlcv: {'model': models.MarketData, 'schema': schemas.MarketData},
    enums.LogType.kalman: {'model': models.KalmanLogEntry, 'schema': schemas.KalmanLogEntry},
    enums.LogType.bot_performance: {'model': models.BotPerformanceLogEntry, 'schema': schemas.BotPerformanceLogEntry}
}


@api.post('/log/', response_model=schemas.OkResponse)
def log(
    payload_type: enums.LogType,
    items: List[Union[schemas.BotPerformanceLogEntry, schemas.KalmanLogEntry, schemas.MarketData]]
) -> schemas.OkResponse:
    """
    Collects OHLCV data, bot perfomance and kalman logs
    """
    schema_class = TYPE_MODEL_MAP[payload_type]['schema']
    if any(not isinstance(item, schema_class) for item in items):
        raise HTTPException(status_code=422, detail=f"all items should be of '{payload_type.value}' type")

    model_class = TYPE_MODEL_MAP[payload_type]['model']
    session.bulk_save_objects(model_class(**item.dict()) for item in items)
    session.commit()
    return schemas.OkResponse()
