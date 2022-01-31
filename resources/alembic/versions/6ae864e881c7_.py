"""empty message

Revision ID: 6ae864e881c7
Revises:
Create Date: 2022-01-31 04:59:59.730959

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6ae864e881c7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("edition", sa.String(length=255), nullable=False),
        sa.Column("should_wipe", sa.BOOLEAN(), nullable=False),
        sa.Column("profile_id", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_id"),
        sa.UniqueConstraint("username"),
    )


def downgrade():
    op.drop_table("accounts")
