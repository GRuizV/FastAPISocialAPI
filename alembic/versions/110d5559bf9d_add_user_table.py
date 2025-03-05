"""add user table

Revision ID: 110d5559bf9d
Revises: 7b7d031650d4
Create Date: 2025-03-04 19:45:33.530124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '110d5559bf9d'
down_revision: Union[str, None] = '7b7d031650d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("users")

    pass
