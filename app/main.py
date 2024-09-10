from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.routers import auth, users
from app.schemas import Message
from security import get_password_hash
from settings import Settings
from alembic import command 
from alembic.config import Config

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}
