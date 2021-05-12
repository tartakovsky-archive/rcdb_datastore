import datetime

from sqlalchemy import Column, DateTime, Float, Integer, BigInteger, Sequence, String, text

from .base import Model


class KalmanLogEntry(Model):
    __tablename__ = 'kalman_log_entries'

    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk
    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()'),
        index=True,
        nullable=False
    )
    name = Column(String(75), index=True, nullable=False)
    price_forex = Column(Float, nullable=False)
    price_crypto = Column(Float, nullable=False)
    ts_data = Column(Integer, nullable=False)
    s1_x = Column(Float, nullable=False)
    s1_P = Column(Float, nullable=False)
    s2_x = Column(Float, nullable=False)
    s2_P = Column(Float, nullable=False)
    s3_x = Column(Float, nullable=False)
    s3_P = Column(Float, nullable=False)
