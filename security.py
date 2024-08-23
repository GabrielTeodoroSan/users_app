from datetime import datetime, timedelta
from http import HTTPStatus
from http.client import HTTPException
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.database import get_session
from app.schemas import TokenData, User
from settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password):
    return PasswordHash.recommended().hash(password)


def password_is_valid(password, hash):
    return PasswordHash.recommended().verify(password, hash)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        HTTPStatus.UNAUTHORIZED,
        'Could not validate credentials.',
        {'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(models.User).where(models.User.email == token_data.username)
    )

    if not user:
        raise credentials_exception

    return user
