"""Add account nickname

Revision ID: 21cf571c901b
Revises: 6ae864e881c7
Create Date: 2022-02-04 21:42:27.708253

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "21cf571c901b"
down_revision = "6ae864e881c7"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "accounts", sa.Column("profile_nickname", sa.String(length=255), nullable=True)
    )


def downgrade():
    op.drop_column("accounts", "profile_nickname")
