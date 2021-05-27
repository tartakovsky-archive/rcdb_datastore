import aioredis

from typing import Union

from sqlalchemy.orm import Session, scoped_session

from db.connection import SessionLocal
from conf.settings import REDIS_URI

SessionType = Union[Session, scoped_session]


def get_session():
    session: SessionType = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


async def get_redis():
    redis = await aioredis.create_redis(REDIS_URI)
    yield redis
