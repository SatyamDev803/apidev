"""add content column to posts tablee

Revision ID: fd783a7510eb
Revises: 6e8bd4583259
Create Date: 2025-05-08 14:15:04.187886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd783a7510eb'
down_revision: Union[str, None] = '6e8bd4583259'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
