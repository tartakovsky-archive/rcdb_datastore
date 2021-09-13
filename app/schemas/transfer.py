from datetime import datetime

from rcdb_commons.lib.schemas.exchange import TransferType
from pydantic import BaseModel, condecimal, constr as standard_constr

from .base import constr
from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class Transfer(BaseModel):
    timestamp: datetime
    symbol: constr(min_length=2, max_length=50, to_upper=True)
    transfer_type: TransferType
    is_sub_account_transfer: bool
    name: standard_constr(min_length=1, max_length=200)
    amount: decimal_type
    amount_usd: decimal_type

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'symbol': 'USDT',
                'name': 'et_bn_sub1',
                'transfer_type': 'MAIN_MARGIN',
                'is_sub_account_transfer': False,
                'amount': 54953.05,
                'amount_usd': 54953.05,
            }
        }
