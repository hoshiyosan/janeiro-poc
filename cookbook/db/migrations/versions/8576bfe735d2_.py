"""empty message

Revision ID: 8576bfe735d2
Revises: f2c883124aa8
Create Date: 2023-10-29 02:04:41.086476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8576bfe735d2'
down_revision: Union[str, None] = 'f2c883124aa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
