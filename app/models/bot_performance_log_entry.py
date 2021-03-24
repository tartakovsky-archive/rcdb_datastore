import datetime

from sqlalchemy import Column, DateTime, BigInteger, Integer, Float, Sequence, text

from .base import Model


class BotPerformanceLogEntry(Model):
    __tablename__ = 'bot_performance_log_entries'

    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk
    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        index=True
    )
    bot_id = Column(Integer, index=True, nullable=False)
    balance_base = Column(Float, nullable=False)
    balance_quote = Column(Float, nullable=False)
    bid = Column(Float, nullable=False)
    ask = Column(Float, nullable=False)
    price_crypto = Column(Float, nullable=False)
    price_fair = Column(Float, nullable=False)
    price_forex = Column(Float, nullable=False)
    balance_base_borrowed = Column(Float, nullable=False)
    balance_quote_borrowed = Column(Float, nullable=False)
