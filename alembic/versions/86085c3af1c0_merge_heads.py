"""merge heads

Revision ID: 86085c3af1c0
Revises: 7d6c9083b3c7, 7ae026599573
Create Date: 2025-09-15 11:37:58.211960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86085c3af1c0'
down_revision: Union[str, Sequence[str], None] = ('7d6c9083b3c7', '7ae026599573')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
