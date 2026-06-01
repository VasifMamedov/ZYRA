"""added category

Revision ID: fb43a3a600cd
Revises: 51b970a34fec
Create Date: 2026-02-02
"""

from alembic import op
import sqlalchemy as sa  # noqa: F401

# revision identifiers, used by Alembic.
revision = "657fb87c4888"
down_revision = "fb43a3a600cd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # No-op placeholder: DB already reflects this change
    pass


def downgrade() -> None:
    # No-op placeholder
    pass