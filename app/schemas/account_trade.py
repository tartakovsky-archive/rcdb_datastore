from datetime import datetime

from pydantic import BaseModel, constr
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import symbol_type
from .mixins import CustomJSONEncoderMixin


class AccountTrade(BaseModel):
    timestamp: datetime
    name: constr(min_length=1, max_length=200)
    symbol: symbol_type
    account_type: AccountType
    volume_buy: float
    volume_sell: float
    volume_base_buy: float
    volume_base_sell: float
    volume_buy_usd: float
    volume_sell_usd: float
    price_avg_buy: float
    price_avg_sell: float
    trades_count_buy: int
    trades_count_sell: int

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'name': 'some name',
                'symbol': 'BTC/USDT',
                'account_type': 'SPOT',
                'volume_buy': 12.5,
                'volume_sell': 15.5,
                'volume_buy_usd': 12.5,
                'volume_sell_usd': 15.5,
                'volume_base_buy_usd': 12.5,
                'volume_base_sell_usd': 15.5,
                'price_avg_buy': 5.5,
                'price_avg_sell': 3.5,
                'trades_count_buy': 10,
                'trades_count_sell': 20,
            }
        }
