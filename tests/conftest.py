import pytest
from fastapi.testclient import TestClient
from jwt import decode
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from testcontainers.postgres import PostgresContainer

from app.database import get_session
from app.main import app
from app.models import User, table_registry
from security import get_password_hash
from settings import Settings


@pytest.fixture
def engine(scope='session'):
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:

        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    user = User(
        username='Bobson',
        email='bobson@gmail.com',
        password=get_password_hash('bobsonfoda123'),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'bobsonfoda123'

    return user

@pytest.fixture
def admin(session):
    user = User(
        username=Settings().ADMIN_NAME,
        email=Settings().ADMIN_EMAIL,
        password=get_password_hash(Settings().ADMIN_PASSWORD),
        admin=True
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'admin'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
