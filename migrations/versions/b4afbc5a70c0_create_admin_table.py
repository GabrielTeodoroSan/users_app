"""create admin table

Revision ID: b4afbc5a70c0
Revises: 2c5428b740af
Create Date: 2024-09-09 21:22:39.904715
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b4afbc5a70c0'
down_revision: Union[str, None] = '2c5428b740af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
