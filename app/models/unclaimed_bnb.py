import datetime

from sqlalchemy import Column, DateTime, Numeric, String, text, BigInteger, Sequence

from .base import Model


class UnclaimedBNB(Model):
    __tablename__ = 'unclaimed_bnb'
    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    name = Column(String(200), nullable=False, index=True)
    unclaimed = Column(Numeric(27, 18, asdecimal=False), nullable=False)
