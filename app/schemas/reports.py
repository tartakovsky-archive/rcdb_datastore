from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, constr
from pydantic.typing import Literal
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import symbol_type
from .mixins import CustomJSONEncoderMixin
from ..enums import RebateCurrency, ReportTimeframe


class ReportParameters(BaseModel):
    report_name: Literal['base_report']

    def get_alchemy_context(self) -> dict:
        raise NotImplementedError()


class TimeframeBasedReportParameters(ReportParameters):
    start_datetime: datetime
    end_datetime: datetime
    timeframe: ReportTimeframe = ReportTimeframe.H

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True

    def get_alchemy_context(self):
        dict_data = self.dict(include={'start_datetime', 'end_datetime', 'timeframe'})

        dict_data['timeframe'] = {
            ReportTimeframe.H: 'hour',
            ReportTimeframe.D: 'day',
            ReportTimeframe.W: 'week',
            ReportTimeframe.M: 'month'
        }[self.timeframe]

        return dict_data


class ReportAccount(BaseModel):
    name: constr(min_length=1, max_length=200)
    account_type: AccountType

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True


class RebateReportParameters(TimeframeBasedReportParameters):
    report_name: Literal['rebate']
    currencies: List[RebateCurrency] = [RebateCurrency.ALL]
    account: Optional[ReportAccount] = None
    excluded_accounts: List[ReportAccount] = []

    def get_alchemy_context(self):
        dict_data = self.dict(exclude={'account', 'excluded_accounts'})

        if RebateCurrency.ALL in self.currencies:
            dict_data['currencies'] = [c.value for c in RebateCurrency]

        dict_data['currencies'] = tuple(dict_data['currencies'])
        dict_data['param_account'] = f'{self.account.name}_{self.account.account_type}' if self.account else None
        dict_data['excluded_accounts'] = tuple(f'{acc.name}_{acc.account_type}' for acc in self.excluded_accounts)
        dict_data['excluded_accounts'] = dict_data['excluded_accounts'] or ('empty',)
        return {**dict_data, **super().get_alchemy_context()}


class PairsVolumeReportParameters(TimeframeBasedReportParameters):
    report_name: Literal['pair_volumes']


class PairsVolumeRow(BaseModel):
    timestamp: datetime
    symbol: symbol_type
    self_volume: float
    market_volume: float
    self_volume_quote: float
    market_volume_quote: float
    pct: float

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True


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


class Report(BaseModel):
    __root__: List[Union[RebateReportRow, PairsVolumeRow]]

    class Config(CustomJSONEncoderMixin):
        use_enum_values = True
