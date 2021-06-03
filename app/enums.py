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
