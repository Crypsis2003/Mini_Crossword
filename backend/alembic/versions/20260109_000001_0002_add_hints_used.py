"""Add hints_used column to solves table

Revision ID: 0002
Revises: 0001
Create Date: 2026-01-09 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add hints_used column to solves table with default 0
    op.add_column('solves', sa.Column('hints_used', sa.Integer(), nullable=True, server_default='0'))


def downgrade() -> None:
    op.drop_column('solves', 'hints_used')
