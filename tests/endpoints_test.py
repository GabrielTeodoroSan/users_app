from sqlalchemy import select

from app.models import User


def test_create_user_endpoint(session, client):
    response = client.post(
        '/create/',
        json={
            'username': 'Bobson',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )

    assert response.status_code == 201


def test_update_user(session, client):
    client.post(
        '/create/',
        json={
            'username': 'Bobson',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )

    response = client.put(
        '/update/1',
        json={
            'username': 'Bobson2',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )
    assert response.status_code == 200


def test_delete_user(session, client):
    client.post(
        '/create/',
        json={
            'username': 'Bobson',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )

    response = client.delete('/delete/1')
    response.status_code == 200


def test_get_user(session, client):
    client.post(
        '/create/',
        json={
            'username': 'Bobson',
            'email': 'bobson@gmail.com',
            'password': 'bobsonorgulhonacional',
        },
    )

    response = client.get('/get/1')

    assert response.status_code == 200
