from http import HTTPStatus
from http.client import HTTPException

from fastapi import Depends, FastAPI
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.database import get_session
from app.schemas import Message, User, UserCreate, UserResponse
from security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):

    db_user = session.scalar(
        select(models.User).where(
            (models.User.username == user.username)
            | (models.User.email == user.email)
        )
    )

    if db_user:
        if user.username == db_user.username:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                'Username already exist !',
            )
        else:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                'Email already exist !',
            )

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.put('/{id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def update_user(
    user: UserCreate,
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN, 'Not enough permissions!'
        )

    updated_user = session.scalar(
        select(models.User).where(models.User.id == id)
    )

    if not updated_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User not exist !'
        )

    updated_user.username = user.username
    updated_user.email = user.email
    update_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(updated_user)

    return updated_user


@router.delete('/{id}', response_model=Message, status_code=HTTPStatus.OK)
def delete_user(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN, 'Not enough permissions!'
        )

    db_user = session.scalar(select(models.User).where(models.User.id == id))

    if not db_user:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, 'User not found'
        )

    return {'message': 'User deleted'}


@router.get('/{id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def get_user(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(models.User).where(models.User.id == id))

    if not db_user:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, 'User not found'
        )

    return db_user
