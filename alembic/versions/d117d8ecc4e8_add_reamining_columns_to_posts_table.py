"""add reamining columns to posts table

Revision ID: d117d8ecc4e8
Revises: b22e5ba2d344
Create Date: 2025-05-08 14:37:44.063563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd117d8ecc4e8'
down_revision: Union[str, None] = 'b22e5ba2d344'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
