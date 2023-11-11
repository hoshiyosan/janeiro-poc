"""add accounts table

Revision ID: 0001
Revises: 
Create Date: 2023-11-11 01:40:25.724233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('uuid', sa.String(length=32), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_accounts_username'), 'accounts', ['username'], unique=True)
    op.create_index(op.f('ix_accounts_uuid'), 'accounts', ['uuid'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_accounts_uuid'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_username'), table_name='accounts')
    op.drop_table('accounts')
    # ### end Alembic commands ###