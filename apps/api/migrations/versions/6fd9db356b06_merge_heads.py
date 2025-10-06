"""merge heads

Revision ID: 6fd9db356b06
Revises: abaca2de82f3, 009191825654
Create Date: 2025-10-06 10:29:09.918325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fd9db356b06'
down_revision: Union[str, Sequence[str], None] = ('abaca2de82f3', '009191825654')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
