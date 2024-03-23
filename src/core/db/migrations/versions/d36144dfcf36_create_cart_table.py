"""Create Cart table

Revision ID: d36144dfcf36
Revises: 641c0d167236
Create Date: 2024-03-23 10:52:34.841370

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d36144dfcf36"
down_revision: Union[str, None] = "641c0d167236"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_products_in_cart_id", table_name="products_in_cart")
    op.drop_table("products_in_cart")
    op.drop_index("ix_products_in_carts_id", table_name="products_in_carts")
    op.drop_table("products_in_carts")
    op.drop_index("ix_products_id", table_name="products")
    op.drop_index("ix_products_name", table_name="products")
    op.drop_table("products")
    op.drop_index("ix_orders_id", table_name="orders")
    op.drop_table("orders")
    op.drop_index("ix_carts_id", table_name="carts")
    op.drop_table("carts")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "carts",
        sa.Column("id", sa.VARCHAR(length=60), autoincrement=False, nullable=False),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "modified_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="carts_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_carts_id", "carts", ["id"], unique=True)
    op.create_table(
        "orders",
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "shipping_address", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column("customer_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "cart_id", sa.VARCHAR(length=60), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.VARCHAR(length=60), autoincrement=False, nullable=False),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "modified_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(["cart_id"], ["carts.id"], name="orders_cart_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="orders_pkey"),
        sa.UniqueConstraint("cart_id", name="orders_cart_id_key"),
    )
    op.create_index("ix_orders_id", "orders", ["id"], unique=True)
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
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_products_name", "products", ["name"], unique=False)
    op.create_index("ix_products_id", "products", ["id"], unique=True)
    op.create_table(
        "products_in_carts",
        sa.Column("quantity", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "product_id", sa.VARCHAR(length=60), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.VARCHAR(length=60), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"], name="products_in_carts_product_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="products_in_carts_pkey"),
    )
    op.create_index("ix_products_in_carts_id", "products_in_carts", ["id"], unique=True)
    op.create_table(
        "products_in_cart",
        sa.Column("id", sa.VARCHAR(length=60), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="products_in_cart_pkey"),
    )
    op.create_index("ix_products_in_cart_id", "products_in_cart", ["id"], unique=True)
    # ### end Alembic commands ###
