import datetime

from sqlalchemy import Column, DateTime, BigInteger, Float, text, Sequence

from .base import Model


class BotPerformanceLogEntry(Model):
    __tablename__ = 'bot_performance_log_entries'

    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk
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
