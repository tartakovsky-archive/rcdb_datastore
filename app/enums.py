from enum import Enum


class LogType(Enum):
    ohlcv = 'ohlcv'
    kalman = 'kalman'
    bot_performance = 'bot_performance'
    price_index = 'price_index'
    account_trades = 'account_trades'


class UpperEnum(Enum):
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


class AccountType(UpperEnum):
    SPOT = 'SPOT'
    FUTURES = 'FUTURES'
    CROSS_MARGIN = 'CROSS_MARGIN'
    ISOLATED_MARGIN = 'ISOLATED_MARGIN'


class Instrument(UpperEnum):
    SPOT = 'SPOT'
    FUTURES = 'FUTURES'
