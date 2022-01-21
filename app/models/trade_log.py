import datetime

from sqlalchemy import Column, DateTime, Integer, text, Sequence, BigInteger, String

from .base import Model


class TradeLog(Model):
    __tablename__ = 'trade_log'
    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    ts_end = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    swap_id = Column(Integer, nullable=False)
    channel = Column(String(500), nullable=False, index=True)
