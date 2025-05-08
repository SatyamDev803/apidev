"""create posts table

Revision ID: 6e8bd4583259
Revises: 
Create Date: 2025-05-08 14:05:17.334746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e8bd4583259'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
