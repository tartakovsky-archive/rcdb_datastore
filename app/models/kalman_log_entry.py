import datetime

from sqlalchemy import Column, DateTime, Float, Integer, BigInteger, Sequence, text

from .base import Model


class KalmanLogEntry(Model):
    __tablename__ = 'kalman_log_entries'

    id_seq = Sequence(f'{__tablename__}_seq')

    id = Column(BigInteger, id_seq, primary_key=True, server_default=id_seq.next_value())  # dummy pk
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
