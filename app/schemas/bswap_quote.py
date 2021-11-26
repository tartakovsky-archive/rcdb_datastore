from datetime import datetime

from pydantic import BaseModel, condecimal

from .base import symbol_type
from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class BSwapQuote(BaseModel):
    timestamp: datetime
    symbol: symbol_type
    price: decimal_type
    slippage: decimal_type
    fee: decimal_type

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'symbol': 'BTC/USDT',
                'price': 54953.05,
                'slippage': 0.00007245,
                'fee': 120
            }
        }
