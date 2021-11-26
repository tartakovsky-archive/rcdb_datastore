import datetime

from sqlalchemy import Column, DateTime, Numeric, String, text, BigInteger, Sequence

from .base import Model


class BSwapQuote(Model):
    __tablename__ = 'bswap_quote'
    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        nullable=False
    )
    symbol = Column(String(50), nullable=False, index=True)

    price = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    slippage = Column(Numeric(27, 18, asdecimal=False), nullable=False)
    fee = Column(Numeric(27, 18, asdecimal=False), nullable=False)
