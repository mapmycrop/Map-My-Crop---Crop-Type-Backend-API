"""update analize table

Revision ID: eb8427ac7b14
Revises: 2f3d31703ddf
Create Date: 2024-06-26 17:45:53.164369

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eb8427ac7b14"
down_revision: Union[str, None] = "2f3d31703ddf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "analize_logs"


def upgrade() -> None:
    op.add_column(
        table_name, sa.Column("title", sa.String(), nullable=False, server_default="")
    )
    op.add_column(
        table_name, sa.Column("country", sa.String(), nullable=False, server_default="")
    )


def downgrade() -> None:
    op.drop_column(table_name, "title")
    op.drop_column(table_name, "country")
