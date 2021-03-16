import datetime
from sqlalchemy import Column, DateTime, Numeric, String, text, Sequence, BigInteger

from .base import Model


class PriceIndex(Model):
    __tablename__ = 'price_indexes'
    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    symbol = Column(String(16), nullable=False, index=True)
    price = Column(Numeric(10, 8, asdecimal=False), nullable=False)
