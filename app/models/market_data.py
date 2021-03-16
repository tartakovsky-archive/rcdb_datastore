import datetime
from sqlalchemy import Column, DateTime, Numeric, String, Enum, text, BigInteger, Sequence

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
    open = Column(Numeric(22, 10, asdecimal=False), nullable=False)
    high = Column(Numeric(22, 10, asdecimal=False), nullable=False)
    low = Column(Numeric(22, 10, asdecimal=False), nullable=False)
    close = Column(Numeric(22, 10, asdecimal=False), nullable=False)
    volume = Column(Numeric(22, 10, asdecimal=False), nullable=False)
