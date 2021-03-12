from datetime import datetime

from pydantic import BaseModel, constr, condecimal

from .mixins import CustomJSONEncoderMixin
from app.enums import Instrument

decimal_type = condecimal(ge=0, max_digits=22, decimal_places=10)
symbol_type = constr(to_lower=True, regex=r'\w+/\w+', max_length=16)


class MarketData(BaseModel):
    timestamp: datetime
    exchange: constr(to_lower=True, min_length=1, max_length=16)
    symbol: symbol_type  # noqa
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
                'exchange': 'binance',
                'symbol': 'btc/usdt',
                'instrument': 'spot',
                'open': 54953.05,
                'high': 54963.05,
                'low': 54933.05,
                'close': 54965.05,
                'volume': 1231254953.05,
            }
        }
