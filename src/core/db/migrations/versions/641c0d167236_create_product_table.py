"""Create product table

Revision ID: 641c0d167236
Revises: 
Create Date: 2024-03-17 11:45:48.898145

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "641c0d167236"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_products_id", table_name="products")
    op.drop_index("ix_products_name", table_name="products")
    op.drop_table("products")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "products",
        sa.Column("name", sa.VARCHAR(length=64), autoincrement=False, nullable=False),
        sa.Column("quantity", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("price", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("image_url", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "modified_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.VARCHAR(length=60), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="products_pkey"),
    )
    op.create_index("ix_products_name", "products", ["name"], unique=False)
    op.create_index("ix_products_id", "products", ["id"], unique=True)
    # ### end Alembic commands ###
