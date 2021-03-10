import datetime

from sqlalchemy import Column, DateTime, Float, Integer, BigInteger, text

from .base import Model


class KalmanLogEntry(Model):
    __tablename__ = 'kalman_log_entries'

    id = Column(BigInteger, autoincrement=True, primary_key=True)  # dummy pk
    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=text('now()')
    )
    price_forex = Column(Float)
    price_crypto = Column(Float)
    ts_data = Column(Integer)
    s1_x = Column(Float)
    s1_P = Column(Float)
    s2_x = Column(Float)
    s2_P = Column(Float)
    s3_x = Column(Float)
    s3_P = Column(Float)
