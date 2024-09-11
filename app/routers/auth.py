from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas import Token
from security import create_access_token, password_is_valid

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token, status_code=HTTPStatus.OK)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            'Incorrect email or password',
        )

    if not password_is_valid(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/admin-access', response_model=Token, status_code=HTTPStatus.OK)
def login_for_admin_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            'Incorrect email or password',
        )

    if not password_is_valid(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Incorrect email or password /{password}',
        )

    if user.admin == False:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='You cant access this content !',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
