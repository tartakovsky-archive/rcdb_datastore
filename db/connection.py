from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from conf.settings import \
    POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, SA_POOL_SIZE, SA_MAX_OVERFLOW

url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
engine = create_engine(
    url,
    pool_size=SA_POOL_SIZE,
    max_overflow=SA_MAX_OVERFLOW,
    pool_pre_ping=True,
    encoding='utf-8'
)


metadata = MetaData()
maker = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
