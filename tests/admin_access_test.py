from http import HTTPStatus

from sqlalchemy import select

from app.models import User
from settings import Settings


def test_if_admin_account_was_created(session, admin):
    adm_user = session.scalar(
        select(User).where(User.email == Settings().ADMIN_EMAIL)
    )

    assert adm_user


def test_if_admin_endpoint_generate_token(session, admin, client):
    response = client.post(
        '/auth/admin-access/',
        data={
            'username': Settings().ADMIN_EMAIL,
            'password': Settings().ADMIN_PASSWORD,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'token_type' in token
    assert 'access_token' in token