from sqlalchemy import select

from app.models import User


def test_create_user_endpoint(session, client):
    response = client.post(
        '/users/',
        json={
            'username': 'Bobson',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )

    assert response.status_code == 201


def test_update_user(session, client, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Bobson2',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )
    assert response.status_code == 200


def test_delete_user(session, client):
    client.post(
        '/users/',
        json={
            'username': 'Bobson',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )

    response = client.delete('/users/1')
    response.status_code == 200


def test_get_user(session, client):
    client.post(
        '/users/',
        json={
            'username': 'Bobson',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )

    response = client.get('/users/1')

    assert response.status_code == 200
