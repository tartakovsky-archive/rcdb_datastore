import datetime

from .base import Model

from sqlalchemy.orm import validates
from sqlalchemy import Column, DateTime, BigInteger, Float, Sequence, text, String
from rcdb_commons.lib.schemas.exchange import AccountType


class Rebate(Model):
    __tablename__ = 'rebates'

    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk
    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        index=True,
        nullable=False
    )
    name = Column(String(200), index=True, nullable=False)
    symbol = Column(String(16), index=True, nullable=False)
    account_type = Column(String(50), index=True, nullable=False)

    rebate = Column(Float)

    @validates('account_type')
    def validate_account_type(self, key, value) -> str:
        try:
            AccountType[value]
            return value
        except KeyError:
            raise AssertionError(f'Wrong account_type value: {value}')
