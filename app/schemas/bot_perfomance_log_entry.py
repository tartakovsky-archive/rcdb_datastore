from datetime import datetime

from pydantic import BaseModel, constr

from .mixins import CustomJSONEncoderMixin


class BotPerformanceLogEntry(BaseModel):
    timestamp: datetime
    name: constr(min_length=1, max_length=16)
    balance_base: float
    balance_quote: float
    bid: float
    ask: float
    price_fair: float
    price_forex: float
    balance_base_borrowed: float
    balance_quote_borrowed: float

    class Config(CustomJSONEncoderMixin):
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'name': 'bot1',
                'balance_base': 25.5,
                'balance_quote': 25.3,
                'bid': 1245.5,
                'ask': 1245.3,
                'price_fair': 1245.45,
                'price_forex': 1245.35,
                'balance_base_borrowed': 100000.5,
                'balance_quote_borrowed': 14555.5
            }
        }
