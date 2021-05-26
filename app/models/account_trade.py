import datetime

from .base import Model

from sqlalchemy.orm import validates
from sqlalchemy import Column, DateTime, BigInteger, Integer, Float, Sequence, text, String
from rcdb_commons.lib.schemas.exchange import AccountType


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
    account_type = Column(String(50), index=True, nullable=False)

    volume_buy = Column(Float, nullable=False)
    volume_sell = Column(Float, nullable=False)
    volume_base_buy = Column(Float, nullable=False)
    volume_base_sell = Column(Float, nullable=False)
    volume_buy_usd = Column(Float, nullable=False)
    volume_sell_usd = Column(Float, nullable=False)
    price_avg_buy = Column(Float, nullable=False)
    price_avg_sell = Column(Float, nullable=False)
    trades_count_buy = Column(Integer, nullable=False)
    trades_count_sell = Column(Integer, nullable=False)

    @validates('account_type')
    def validate_account_type(self, key, value) -> str:
        try:
            AccountType[value]
            return value
        except KeyError:
            raise AssertionError(f'Wrong account_type value: {value}')
