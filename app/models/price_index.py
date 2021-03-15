import datetime
from sqlalchemy import Column, DateTime, Numeric, String, text

from .base import Model


class PriceIndex(Model):
    __tablename__ = 'price_indexes'

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        primary_key=True
    )
    symbol = Column(String(16), primary_key=True)
    price = Column(Numeric(10, 8, asdecimal=False), nullable=False)
