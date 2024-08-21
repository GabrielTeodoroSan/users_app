from sqlalchemy import select

from app.models import User


def test_create_user(session):
    new_user = User(
        username='Boberson',
        email='boberson@gmail.com',
        password='1234Testando',
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Boberson'))

    assert user.username == 'Boberson'
