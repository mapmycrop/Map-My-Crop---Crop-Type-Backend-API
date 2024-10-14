"""add analize_log table

Revision ID: 2f3d31703ddf
Revises: 2db9f9fa812b
Create Date: 2024-06-19 17:38:22.168582

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f3d31703ddf"
down_revision: Union[str, None] = "2db9f9fa812b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "analize_logs"


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("feature_count", sa.Integer(), nullable=True),
        sa.Column("area_count", sa.Float(), nullable=True),
        sa.Column("table_name", sa.String(), nullable=True),
        sa.Column(
            "time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table(table_name)
