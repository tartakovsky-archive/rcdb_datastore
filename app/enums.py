from enum import Enum


class UpperEnumMixin:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, (str, cls)):
            raise TypeError(f'Expected str/{cls.__name__} {type(v)}')

        if isinstance(v, str):
            v = v.upper()
            if hasattr(cls, v):
                return getattr(cls, v)
            else:
                raise ValueError(f'Unexpected {cls.__name__} value: {v}')
        else:
            return v

    def __getitem__(self, item):
        return super().__getitem__(item.upper())


class Instrument(UpperEnumMixin, Enum):
    SPOT = 'SPOT'
    FUTURES = 'FUTURES'


class RebateCurrency(UpperEnumMixin, Enum):
    ALL = 'ALL'
    EUR = 'EUR'
    GBP = 'GBP'
    BRL = 'BRL'
    TRY = 'TRY'
    RUB = 'RUB'
    UAH = 'UAH'
    AUD = 'AUD'


class ReportTimeframe(UpperEnumMixin, Enum):
    H = 'H'
    D = 'D'
    W = 'W'
    M = 'M'


class TransferType(UpperEnumMixin, Enum):
    MAIN_C2C = 'MAIN_C2C'
    MAIN_UMFUTURE = 'MAIN_UMFUTURE'
    MAIN_CMFUTURE = 'MAIN_CMFUTURE'
    MAIN_MARGIN = 'MAIN_MARGIN'
    MAIN_MINING = 'MAIN_MINING'
    C2C_MAIN = 'C2C_MAIN'
    C2C_UMFUTURE = 'C2C_UMFUTURE'
    C2C_MARGIN = 'C2C_MARGIN'
    UMFUTURE_MAIN = 'UMFUTURE_MAIN'
    UMFUTURE_C2C = 'UMFUTURE_C2C'
    UMFUTURE_MARGIN = 'UMFUTURE_MARGIN'
    CMFUTURE_MAIN = 'CMFUTURE_MAIN'
    CMFUTURE_MARGIN = 'CMFUTURE_MARGIN'
    MARGIN_MAIN = 'MARGIN_MAIN'
    MARGIN_UMFUTURE = 'MARGIN_UMFUTURE'
    MARGIN_CMFUTURE = 'MARGIN_CMFUTURE'
    MARGIN_MINING = 'MARGIN_MINING'
    MARGIN_C2C = 'MARGIN_C2C'
    MINING_MAIN = 'MINING_MAIN'
    MINING_UMFUTURE = 'MINING_UMFUTURE'
    MINING_C2C = 'MINING_C2C'
    MINING_MARGIN = 'MINING_MARGIN'
    MAIN_PAY = 'MAIN_PAY'
    PAY_MAIN = 'PAY_MAIN'
    MAIN_DEPOSIT = 'MAIN_DEPOSIT'
    MAIN_WITHDRAWAL = 'MAIN_WITHDRAWAL'

    @classmethod
    def external_transfers(cls) -> set:
        return {cls.MAIN_DEPOSIT, cls.MAIN_WITHDRAWAL}
