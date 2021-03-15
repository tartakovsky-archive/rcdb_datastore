from enum import Enum


class LogType(Enum):
    ohlcv = 'ohlcv'
    kalman = 'kalman'
    bot_performance = 'bot_performance'
    price_index = 'price_index'


class Instrument(Enum):
    spot = 'spot'
    futures = 'futures'
