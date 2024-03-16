from pydantic import BaseModel
from shop.product.domain import Currency

class ProductSchema(BaseModel):
    quantity: int
    price: int
    currency: Currency
    id: str
    name: str
    description: str | None = None
    image_url: str | None = None