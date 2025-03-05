"""create post table

Revision ID: 4ef7e76f6f5b
Revises: 
Create Date: 2025-03-04 19:27:19.648527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ef7e76f6f5b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table('posts')
    
    pass
