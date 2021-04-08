import datetime

from .base import Model

from sqlalchemy import Column, DateTime, BigInteger, Integer, Float, Sequence, text, String


class AccountTrade(Model):
    __tablename__ = 'account_trades'

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

    volume_buy = Column(Float, nullable=False)
    volume_sell = Column(Float, nullable=False)
    price_avg_buy = Column(Float, nullable=False)
    price_avg_sell = Column(Float, nullable=False)
    trades_count_buy = Column(Integer, nullable=False)
    trades_count_sell = Column(Integer, nullable=False)
