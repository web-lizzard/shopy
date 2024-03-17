from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base, TimestampMixin, IdentifierMixin

class Product(Base, TimestampMixin, IdentifierMixin):
    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String(length=64), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

