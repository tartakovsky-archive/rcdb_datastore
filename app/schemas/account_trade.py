from datetime import datetime

from pydantic import BaseModel, constr

from .base import symbol_type
from .mixins import CustomJSONEncoderMixin


class AccountTrade(BaseModel):
    timestamp: datetime
    name: constr(min_length=1, max_length=200)
    symbol: symbol_type
    volume_buy: float
    volume_sell: float
    price_avg_buy: float
    price_avg_sell: float
    trades_count_buy: int
    trades_count_sell: int

    class Config(CustomJSONEncoderMixin):
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'name': 'some name',
                'symbol': 'BTC/USDT',
                'volume_buy': 12.5,
                'volume_sell': 15.5,
                'price_avg_buy': 5.5,
                'price_avg_sell': 3.5,
                'trades_count_buy': 10,
                'trades_count_sell': 20,
            }
        }
