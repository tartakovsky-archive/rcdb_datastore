from datetime import datetime

from pydantic import BaseModel, condecimal
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import exchange_type, symbol_type
from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class BidAsk(BaseModel):
    timestamp: datetime
    exchange: exchange_type
    symbol: symbol_type
    account_type: AccountType
    bid: decimal_type
    ask: decimal_type

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'exchange': 'BINANCE',
                'symbol': 'BTC/USDT',
                'account_type': 'SPOT',
                'bid': 54953.05,
                'ask': 54963.05,
            }
        }
