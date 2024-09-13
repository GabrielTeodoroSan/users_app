"""new admin row

Revision ID: c0eb5186461b
Revises: b4afbc5a70c0
Create Date: 2024-09-10 17:17:26.360007
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c0eb5186461b'
down_revision: Union[str, None] = 'b4afbc5a70c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=False))
    op.create_index('users_email_index', 'users', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('users_email_index', table_name='users')
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###
