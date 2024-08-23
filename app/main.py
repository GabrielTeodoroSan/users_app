from http import HTTPStatus
from http.client import HTTPException

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.database import get_session
from app.schemas import Message, User, UserCreate, UserResponse

app = FastAPI()


@app.post(
    '/create/', response_model=UserResponse, status_code=HTTPStatus.CREATED
)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    new_user = models.User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.put(
    '/update/{id}', response_model=UserResponse, status_code=HTTPStatus.OK
)
def update_user(
    user: UserCreate, id: int, session: Session = Depends(get_session)
):
    updated_user = session.scalar(
        select(models.User).where(models.User.id == id)
    )

    updated_user.username = user.username
    updated_user.email = user.email
    update_user.password = user.password

    session.commit()
    session.refresh(updated_user)

    return updated_user


@app.delete('/delete/{id}', response_model=Message, status_code=HTTPStatus.OK)
def delete_user(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(models.User).where(models.User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return {'message': 'User deleted'}


@app.get('/get/{id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def get_user(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(models.User).where(models.User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user
