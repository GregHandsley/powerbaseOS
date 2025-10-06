"""floorplan table

Revision ID: f11abc7079a3
Revises: d5fa5364d20e
Create Date: 2025-10-06 12:04:07.742869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f11abc7079a3'
down_revision: Union[str, Sequence[str], None] = 'd5fa5364d20e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create unique constraint only if it does not already exist (by name)
    bind = op.get_bind()
    exists = bind.exec_driver_sql(
        "SELECT 1 FROM pg_constraint WHERE conname = 'uq_user_role'"
    ).scalar()
    if not exists:
        op.create_unique_constraint("uq_user_role", "user_roles", ["user_id", "role_id"])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop unique constraint only if it exists (by name)
    bind = op.get_bind()
    exists = bind.exec_driver_sql(
        "SELECT 1 FROM pg_constraint WHERE conname = 'uq_user_role'"
    ).scalar()
    if exists:
        op.drop_constraint("uq_user_role", "user_roles", type_="unique")
