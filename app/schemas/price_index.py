from datetime import datetime

from pydantic import BaseModel, condecimal

from .mixins import CustomJSONEncoderMixin
from .market_data import symbol_type


class PriceIndex(BaseModel):
    timestamp: datetime
    symbol: symbol_type  # noqa
    price: condecimal(ge=0, max_digits=10, decimal_places=8)

    class Config(CustomJSONEncoderMixin):
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'symbol': 'gbp/busd',
                'price': 1.3900009,
            }
        }
