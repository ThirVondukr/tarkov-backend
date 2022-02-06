"""Make nickname not nullable, add unique constraints

Revision ID: 939371a7b93f
Revises: 21cf571c901b
Create Date: 2022-02-06 12:33:23.173408

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "939371a7b93f"
down_revision = "21cf571c901b"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.alter_column(
            "profile_id", existing_type=sa.VARCHAR(length=64), nullable=False
        )
        batch_op.create_unique_constraint("uq_profile_id", ["profile_id"])
        batch_op.create_unique_constraint("uq_profile_nickname", ["profile_nickname"])
        batch_op.create_unique_constraint("uq_username", ["username"])


def downgrade():
    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.drop_constraint("uq_username", type_="unique")
        batch_op.drop_constraint("uq_profile_nickname", type_="unique")
        batch_op.drop_constraint("uq_profile_id", type_="unique")
        batch_op.alter_column(
            "profile_id", existing_type=sa.VARCHAR(length=64), nullable=True
        )
