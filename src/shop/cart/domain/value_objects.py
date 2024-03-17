from enum import StrEnum
from dataclasses import dataclass
from shop.product.domain import Product, Quantity

class CartState(StrEnum):
    CREATED = 'created'
    EXECUTED = 'executed'
    NOT_ACTIVE = 'not_active'

@dataclass(frozen=True)
class OrderInfo:
    email: str
    address: str

@dataclass()
class ProductInCart:
    product: Product
    quantity: Quantity