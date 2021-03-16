from typing import Union

from sqlalchemy.orm import Session, scoped_session

from .connection import SessionLocal


session: Union[Session, scoped_session] = scoped_session(SessionLocal)
