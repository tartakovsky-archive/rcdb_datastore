import datetime

from sqlalchemy.orm import validates
from sqlalchemy import Column, DateTime, Numeric, String, text, BigInteger, Sequence
from rcdb_commons.lib.schemas.exchange import TransferType

from .base import Model


class Transfer(Model):
    __tablename__ = 'transfers'
    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    symbol = Column(String(50), nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    transfer_type = Column(String(50), nullable=False, index=True)
    amount = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    amount_usd = Column(Numeric(27, 18, asdecimal=False), nullable=False)

    @validates('transfer_type')
    def validate_transfer_type(self, key, value) -> str:
        try:
            TransferType[value]
            return value
        except KeyError:
            raise AssertionError(f'Wrong transfer_type value: {value}')
