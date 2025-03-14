"""Initial migration

Revision ID: e131f50e6a38
Revises: dce9b771cd48
Create Date: 2025-03-14 14:04:58.831774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e131f50e6a38'
down_revision: Union[str, None] = 'dce9b771cd48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
