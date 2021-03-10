import datetime

from sqlalchemy import Column, DateTime, BigInteger, Float, text

from .base import Model


class BotPerformanceLogEntry(Model):
    __tablename__ = 'bot_performance_log_entries'

    id = Column(BigInteger, autoincrement=True, primary_key=True)  # dummy pk
    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
    )
    balance_base = Column(Float)
    balance_quote = Column(Float)
    bid = Column(Float)
    ask = Column(Float)
    price_fair = Column(Float)
    price_forex = Column(Float)
    balance_base_borrowed = Column(Float)
    balance_quote_borrowed = Column(Float)
