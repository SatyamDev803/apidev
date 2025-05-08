"""add foregin-key to posts table

Revision ID: b22e5ba2d344
Revises: 0bf4e61758cf
Create Date: 2025-05-08 14:29:07.143352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b22e5ba2d344'
down_revision: Union[str, None] = '0bf4e61758cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
