from datetime import datetime

from pydantic import BaseModel, constr
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import symbol_type
from .mixins import CustomJSONEncoderMixin


class Rebate(BaseModel):
    timestamp: datetime
    name: constr(min_length=1, max_length=200)
    symbol: symbol_type
    account_type: AccountType
    rebate: float
    rebate_usd: float

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'name': 'some name',
                'symbol': 'EUR',
                'account_type': 'SPOT',
                'rebate': 12.5,
                'rebate_usd': 15.5,
            }
        }
