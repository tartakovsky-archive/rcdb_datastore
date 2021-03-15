from enum import Enum


class LogType(Enum):
    ohlcv = 'ohlcv'
    kalman = 'kalman'
    bot_performance = 'bot_performance'
    price_index = 'price_index'


class Instrument(Enum):
    SPOT = 'SPOT'
    FUTURES = 'FUTURES'

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, (str, cls)):
            raise TypeError(f'Expected str/Instrument {type(v)}')

        if isinstance(v, str):
            v = v.upper()
            if hasattr(cls, v):
                return getattr(cls, v)
            else:
                raise ValueError(f'Unexpected instrument value: {v}')
        else:
            return v

    def __getitem__(self, item):
        return super().__getitem__(item.upper())
