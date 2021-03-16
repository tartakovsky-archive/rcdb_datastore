from typing import Union

from sqlalchemy.orm import Session, scoped_session

from db.connection import maker


SessionType = Union[Session, scoped_session]


def get_session():
    session: SessionType = scoped_session(maker)
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.remove()
