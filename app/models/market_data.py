import datetime

from sqlalchemy.orm import validates
from sqlalchemy import Column, DateTime, Numeric, String, Enum, text, BigInteger, Sequence
from rcdb_commons.lib.schemas.exchange import AccountType

from .base import Model
from app.enums import Instrument


class MarketData(Model):
    __tablename__ = 'markets_data'
    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    exchange = Column(String(16), nullable=False, index=True)
    symbol = Column(String(16), nullable=False, index=True)
    instrument = Column(Enum(Instrument, native_enum=False), nullable=False, index=True)
    account_type = Column(String(50), nullable=True)
    open = Column(Numeric(22, 10, asdecimal=False), nullable=False)
    high = Column(Numeric(22, 10, asdecimal=False), nullable=False)
    low = Column(Numeric(22, 10, asdecimal=False), nullable=False)
    close = Column(Numeric(22, 10, asdecimal=False), nullable=False)
    volume = Column(Numeric(22, 10, asdecimal=False), nullable=False)

    @validates('account_type')
    def validate_account_type(self, key, value) -> str:
        try:
            if value:
                AccountType[value]
            return value
        except KeyError:
            raise AssertionError(f'Wrong account_type value: {value}')
