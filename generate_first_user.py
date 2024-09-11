from app.database import get_session
from app.models import User
from sqlalchemy import select
from security import get_password_hash

from settings import Settings


def generate_admin_user():
    session = next(get_session())

    user_admin = session.scalar(
        select(User).where(User.username == Settings().ADMIN_NAME)
    )

    if user_admin:
        return 'User admin already exist'
    
    user_admin = User(
        username=Settings().ADMIN_NAME,
        email=Settings().ADMIN_EMAIL,
        password=get_password_hash(Settings().ADMIN_PASSWORD),
        admin=True,
    )

    session.add(user_admin)
    session.commit()
    session.refresh(user_admin)

    return f'{user_admin.password}'


print(generate_admin_user())
