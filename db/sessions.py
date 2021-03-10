from typing import Union

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from conf.settings import POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT

url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
engine = create_engine(
    url,
    convert_unicode=True,
    pool_size=10,
    max_overflow=10,
    pool_pre_ping=True,
    encoding='utf-8',
)


metadata = MetaData()
maker = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
session: Union[Session, scoped_session] = scoped_session(maker)
