from sqlalchemy import (
    String,
    Text,
    Integer,
    ForeignKey,
    Enum,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from shop.cart.domain import CartState

from core.db import Base, TimestampMixin, IdentifierMixin

cart_state = tuple(state.value for state in CartState)
cart_state_enum = Enum(*cart_state, name="State of a cart", default=CartState.CREATED)


class Product(Base, TimestampMixin, IdentifierMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(length=64), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    carts: Mapped[list["ProductInCart"]] = relationship()


class Cart(Base, IdentifierMixin, TimestampMixin):
    __tablename__ = "carts"

    expired_at: Mapped[datetime] = mapped_column(DateTime)
    cart_state: Mapped[CartState] = mapped_column(cart_state_enum)
    products_in_cart: Mapped[list["ProductInCart"]] = relationship()
    order_info: Mapped["OrderInfo | None"] = relationship(back_populates="cart")


class ProductInCart(Base, IdentifierMixin):
    __tablename__ = "products_in_carts"

    quantity: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="carts")
    cart: Mapped["Cart"] = relationship(back_populates="products_in_cart")
    cart_id: Mapped[str] = mapped_column(ForeignKey("carts.id"))


class OrderInfo(Base, IdentifierMixin, TimestampMixin):
    __tablename__ = "orders"

    email: Mapped[str] = mapped_column(String)
    shipping_address: Mapped[str] = mapped_column(String)
    customer_name: Mapped[str] = mapped_column(String)
    cart: Mapped["Cart"] = relationship(back_populates="order_info", single_parent=True)
    cart_id: Mapped[str] = mapped_column(ForeignKey("carts.id"))

    __table_args__ = (UniqueConstraint("cart_id"),)
