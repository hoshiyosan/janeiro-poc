"""empty message

Revision ID: f2c883124aa8
Revises: eb2792d13f5a
Create Date: 2023-10-29 02:59:34.269459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2c883124aa8'
down_revision: Union[str, None] = 'eb2792d13f5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
