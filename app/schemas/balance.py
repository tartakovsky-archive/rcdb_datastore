from datetime import datetime

from pydantic import BaseModel, condecimal
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import constr
from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class Balance(BaseModel):
    timestamp: datetime
    symbol: constr(min_length=2, max_length=50, to_upper=True)
    account_type: AccountType
    amount: decimal_type
    amount_usd: decimal_type
    borrowed: decimal_type
    borrowed_usd: decimal_type
    interest: decimal_type
    interest_usd: decimal_type

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'symbol': 'BTC',
                'account_type': 'SPOT',
                'amount': 54953.05,
                'amount_usd': 54953.05,
                'borrowed': 54953.05,
                'borrowed_usd': 54953.05,
                'interest': 54953.05,
                'interest_usd': 54963.05
            }
        }
