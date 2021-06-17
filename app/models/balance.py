import datetime

from sqlalchemy.orm import validates
from sqlalchemy import Column, DateTime, Numeric, String, text, BigInteger, Sequence
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import Model


class Balance(Model):
    __tablename__ = 'balances'
    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    symbol = Column(String(50), nullable=False, index=True)
    account_type = Column(String(50), nullable=False, index=True)
    amount = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    amount_usd = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    borrowed = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    borrowed_usd = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    interest = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    interest_usd = Column(Numeric(27, 18, asdecimal=False), nullable=False)

    @validates('account_type')
    def validate_account_type(self, key, value) -> str:
        try:
            AccountType[value]
            return value
        except KeyError:
            raise AssertionError(f'Wrong account_type value: {value}')
