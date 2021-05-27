import time

from pydantic import BaseModel

from .base import symbol_type
from .mixins import CustomJSONEncoderMixin


class ForexPrice(BaseModel):
    timestamp: int
    symbol: symbol_type
    bid: float
    ask: float

    class Config(CustomJSONEncoderMixin):
        schema_extra = {
            'example': {
                'timestamp': int(time.time()),
                'symbol': 'EUR/USD',
                'bid': 1.1,
                'ask': 1.2
            }
        }
