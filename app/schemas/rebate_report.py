from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, constr
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import symbol_type
from .mixins import CustomJSONEncoderMixin
from ..enums import RebateCurrency, RebateReportTimeframe


class ReportAccount(BaseModel):
    name: constr(min_length=1, max_length=200)
    account_type: AccountType

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True


class RebateReportParameters(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    timeframe: RebateReportTimeframe = RebateReportTimeframe.H
    currencies: List[RebateCurrency] = [RebateCurrency.ALL]
    account: Optional[ReportAccount] = None
    excluded_accounts: List[ReportAccount] = []

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True

    @property
    def alchemy_context(self):
        dict_data = self.dict(exclude={'timeframe', 'account', 'excluded_accounts'})

        if RebateCurrency.ALL in self.currencies:
            dict_data['currencies'] = [c.value for c in RebateCurrency]

        dict_data['currencies'] = tuple(dict_data['currencies'])

        dict_data['timeframe'] = {
            RebateReportTimeframe.H: 'hour',
            RebateReportTimeframe.D: 'day',
            RebateReportTimeframe.W: 'week',
            RebateReportTimeframe.M: 'month'
        }[self.timeframe]
        dict_data['param_account'] = f'{self.account.name}_{self.account.account_type}' if self.account else None
        dict_data['excluded_accounts'] = tuple(f'{acc.name}_{acc.account_type}' for acc in self.excluded_accounts)
        dict_data['excluded_accounts'] = dict_data['excluded_accounts'] or ('empty',)
        return dict_data


class RebateReportRow(BaseModel):
    timestamp: datetime
    name: constr(min_length=1, max_length=200)
    symbol: symbol_type
    account_type: AccountType
    volume: float
    expected_rebate: float
    rebate: float
    difference: float
    volume_usd: float
    expected_rebate_usd: float
    rebate_usd: float
    difference_usd: float

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'name': 'some name',
                'symbol': 'EUR',
                'account_type': 'SPOT',
                'volume': 100,
                'expected_rebate': 5.5,
                'rebate': 5.0,
                'difference': -0.5,
                'volume_usd': 150,
                'expected_rebate_usd': 7.5,
                'rebate_usd': 7.0,
                'difference_usd': -0.5
            }
        }


class RebateReport(BaseModel):
    __root__: List[RebateReportRow]

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
        schema_extra = {
            'example': [
                {
                    'timestamp': datetime.utcnow(),
                    'name': 'some name',
                    'symbol': 'EUR',
                    'account_type': 'SPOT',
                    'volume': 100,
                    'expected_rebate': 5.5,
                    'rebate': 5.0,
                    'difference': -0.5,
                    'volume_usd': 150,
                    'expected_rebate_usd': 7.5,
                    'rebate_usd': 7.0,
                    'difference_usd': -0.5
                }
            ]
        }
