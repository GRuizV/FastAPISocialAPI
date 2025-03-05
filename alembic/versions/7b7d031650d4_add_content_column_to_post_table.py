"""Add content column to post table

Revision ID: 7b7d031650d4
Revises: 4ef7e76f6f5b
Create Date: 2025-03-04 19:37:43.433707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b7d031650d4'
down_revision: Union[str, None] = '4ef7e76f6f5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("posts", 'content')
    
    pass
