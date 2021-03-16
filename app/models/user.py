from sqlalchemy import Column, String, Integer, Boolean, text

from .base import Model


class User(Model):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    username = Column(String(64), nullable=False, unique=True, index=True)
    password = Column(String(200), nullable=False)

    is_active = Column(Boolean, nullable=False, default=True, server_default=text('TRUE'))
