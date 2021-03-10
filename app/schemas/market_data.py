from datetime import datetime

from pydantic import BaseModel, constr, condecimal

decimal_type = condecimal(ge=0, max_digits=22, decimal_places=10)


class MarketData(BaseModel):
    timestamp: datetime
    exchange: str
    symbol: constr(to_lower=True, regex=r'\w+/\w+')  # noqa
    open: decimal_type
    high: decimal_type
    low: decimal_type
    close: decimal_type
    volume: decimal_type

    class Config:
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'exchange': 'binance',
                'symbol': 'btc/usdt',
                'open': 54953.05,
                'high': 54963.05,
                'low': 54933.05,
                'close': 54965.05,
                'volume': 1231254953.05,
            }
        }
