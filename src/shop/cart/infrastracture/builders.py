import abc
from ..domain import OrderInfo, Cart, ProductInCart, ProductsInCart
from shop.product.domain import Money, Product, Quantity
from shop.product.infrastructure import ProductBuilder
from ...models import OrderInfo as OrderInfoModel, ProductInCart as ProductInCartModel, Cart as CartModel, Product as ProductModel

class OrderInfoBuilder:
    def __init__(self, model: OrderInfoModel) -> None:
        self._model = OrderInfo(email=model.email, shipping_address=model.shipping_address, customer_name=model.customer_name)

    def build(self) -> OrderInfo:
        return self._model

class ProductsInCartBuilder:
    def __init__(self, model: list[ProductInCartModel]) -> None:
        products = [ProductInCart(product=ProductBuilder(p.product).build(), quantity=Quantity(p.quantity)) for p in model]

        self._model = ProductsInCart(products)

    def build(self) -> ProductsInCart:
        return self._model
    
class CartBuilder:
    def __init__(self, model: CartModel) -> None:
        products_in_cart_builder = ProductsInCartBuilder(model.products_in_cart)
        order_info_builder = OrderInfoBuilder(model.order_info) if model.order_info else None
        self._model = Cart(id=model.id, 
                           products_in_cart=products_in_cart_builder.build(),
                             order_info=order_info_builder.build() if order_info_builder else None, 
                             cart_state=model.cart_state,
                             modified_at=model.modified_at,
                             expired_at=model.expired_at,
                            created_at=model.created_at,

                             )
        
    def build(self) -> Cart:
        return self._model
    