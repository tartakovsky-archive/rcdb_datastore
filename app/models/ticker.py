import datetime

from sqlalchemy import Column, DateTime, Numeric, String, text, BigInteger, Sequence, Boolean

from .base import Model


class Ticker(Model):
    __tablename__ = 'ticker'
    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    channel = Column(String(500), nullable=False, index=True)

    p = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    q = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    bm = Column(Boolean, nullable=False)
