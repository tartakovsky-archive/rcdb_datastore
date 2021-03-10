import datetime
from sqlalchemy import Column, DateTime, Numeric, String, text

from .base import Model


class MarketData(Model):
    __tablename__ = 'markets_data'

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        primary_key=True
    )
    exchange = Column(String(16), primary_key=True)
    symbol = Column(String(16), primary_key=True)
    open = Column(Numeric(22, 10), nullable=False)
    high = Column(Numeric(22, 10), nullable=False)
    low = Column(Numeric(22, 10), nullable=False)
    close = Column(Numeric(22, 10), nullable=False)
    volume = Column(Numeric(22, 10), nullable=False)
