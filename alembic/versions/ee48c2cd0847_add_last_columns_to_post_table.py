"""add last columns to post table

Revision ID: ee48c2cd0847
Revises: 7cd7a2319517
Create Date: 2025-03-04 21:52:05.307824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee48c2cd0847'
down_revision: Union[str, None] = '7cd7a2319517'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))

    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")

    pass
