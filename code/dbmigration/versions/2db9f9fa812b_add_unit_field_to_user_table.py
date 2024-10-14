"""add unit field to user table

Revision ID: 2db9f9fa812b
Revises: f7544cc6db55
Create Date: 2024-06-18 22:08:36.986810

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2db9f9fa812b"
down_revision: Union[str, None] = "f7544cc6db55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "users"


def upgrade() -> None:
    unit_type_enum = sa.Enum("metric", "imperial", name="unit_source")
    unit_type_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        table_name,
        sa.Column(
            "unit",
            unit_type_enum,
            nullable=False,
            server_default="metric",
        ),
    )


def downgrade() -> None:
    op.drop_column(table_name, "unit")
