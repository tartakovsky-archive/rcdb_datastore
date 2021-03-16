from typing import Optional

import jwt
from passlib.hash import pbkdf2_sha256
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials, OAuth2PasswordRequestForm

from app import models, schemas
from app.views.depends import get_session, SessionType
from conf.settings import SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_user(
    username: str,
    session: SessionType = Depends(get_session)
) -> Optional[schemas.UserDB]:
    user: models.User = (
        session
        .query(models.User)
        .filter(models.User.username == username)
        .first()
    )

    if user:
        return schemas.UserDB(**user.to_dict())


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def decode_token(
    token: str,
    session: SessionType = Depends(get_session)
) -> Optional[schemas.UserDB]:
    data = jwt.decode(token, SECRET, algorithms='HS256')
    if data and 'id' in data:
        user: models.User = session.query(models.User).get(data['id'])
        if user:
            return schemas.UserDB(**user.to_dict())


def encode_token(user: schemas.UserDB) -> str:
    return jwt.encode({'id': user.id}, SECRET, algorithm='HS256')


def check_password(user: schemas.UserDB, password: str) -> bool:
    return pbkdf2_sha256.verify(password, user.password)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: SessionType = Depends(get_session)
) -> schemas.UserDB:
    user: Optional[schemas.UserDB] = decode_token(token, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user


def get_current_active_user(current_user: schemas.UserDB = Depends(get_current_user)) -> schemas.UserDB:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')
    return current_user


def create_user(
    username: str,
    password: str,
    is_active: bool = True,
    drop: bool = True,
    session: SessionType = Depends(get_session)
) -> schemas.User:
    old_user = session.query(models.User).filter(models.User.username == username).first()
    if old_user:
        session.delete(old_user)
        session.commit()

    user = models.User(username=username, password=hash_password(password), is_active=is_active)
    session.add(user)
    session.commit()
    return schemas.UserDB(**user.to_dict())


security = HTTPBasic()


def get_current_active_user_basic_auth(
    credentials: HTTPBasicCredentials = Depends(security),
    session: SessionType = Depends(get_session)
):
    user: Optional[schemas.UserDB] = get_user(credentials.username, session=session)
    if user and check_password(user, credentials.password) and user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Basic'},
    )


def get_current_active_user_token_auth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: SessionType = Depends(get_session)
):
    user: Optional[schemas.UserDB] = get_user(form_data.username, session=session)
    if user and check_password(user, form_data.password) and user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Incorrect username or password'
    )
