from datetime import datetime

from pydantic import BaseModel, condecimal

from .base import exchange_type, symbol_type
from .mixins import CustomJSONEncoderMixin
from app.enums import Instrument

decimal_type = condecimal(max_digits=22, decimal_places=10)


class MarketData(BaseModel):
    timestamp: datetime
    exchange: exchange_type
    symbol: symbol_type
    instrument: Instrument
    open: decimal_type
    high: decimal_type
    low: decimal_type
    close: decimal_type
    volume: decimal_type

    class Config(CustomJSONEncoderMixin):
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'exchange': 'BINANCE',
                'symbol': 'BTC/USDT',
                'instrument': 'spot',
                'open': 54953.05,
                'high': 54963.05,
                'low': 54933.05,
                'close': 54965.05,
                'volume': 1231254953.05,
            }
        }
