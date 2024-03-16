from .schemas import ProductSchema
from shop.product.domain import Product


def convert_product_to_schema(product: Product) -> ProductSchema:
    return ProductSchema(name=product.name,
                        quantity=product.quantity.value, 
                         price=product.price.amount, 
                         currency=product.price.currency, description=product.description, 
                         image_url=product.image_url, 
                         id=product.id)
