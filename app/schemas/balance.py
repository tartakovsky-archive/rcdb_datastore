from datetime import datetime

from pydantic import BaseModel, condecimal, constr as standard_constr
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import constr
from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class Balance(BaseModel):
    timestamp: datetime
    symbol: constr(min_length=2, max_length=50, to_upper=True)
    account_type: AccountType
    name: standard_constr(min_length=1, max_length=200)
    amount: decimal_type
    amount_usd: decimal_type
    borrowed: decimal_type
    borrowed_usd: decimal_type
    interest: decimal_type
    interest_usd: decimal_type
    free: decimal_type
    free_usd: decimal_type

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'symbol': 'BTC',
                'name': 'et_bn_sub1',
                'account_type': 'SPOT',
                'amount': 54953.05,
                'amount_usd': 54953.05,
                'borrowed': 54953.05,
                'borrowed_usd': 54953.05,
                'interest': 54953.05,
                'interest_usd': 54963.05,
                'free': 54953.05,
                'free_usd': 54963.05
            }
        }
