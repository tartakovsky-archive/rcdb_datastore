from datetime import datetime

from pydantic import BaseModel, condecimal

from .base import symbol_type
from .mixins import CustomJSONEncoderMixin


class PriceIndex(BaseModel):
    timestamp: datetime
    symbol: symbol_type
    price: condecimal(ge=0, max_digits=10, decimal_places=8)

    class Config(CustomJSONEncoderMixin):
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'symbol': 'gbp/busd',
                'price': 1.3900009,
            }
        }
