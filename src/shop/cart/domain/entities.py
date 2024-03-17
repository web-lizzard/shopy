from dataclasses import dataclass, field
from datetime import datetime
import functools

from shop.product.domain import Quantity , Money
from .value_objects import ProductInCart, CartState, OrderInfo


@dataclass
class ProductsInCart:
    products: list[ProductInCart] = field(default_factory=list)

    @property
    def total_cost(self) -> Money:
        return functools.reduce(lambda price, product : price + product.product.price * product.quantity, self.products, Money(0))
    
    def add_product(self, product: ProductInCart):
        product_in_cart = self.find_product(product)

        if product_in_cart is None:
            return self.products.append(product)
        
        product_in_cart.quantity += product.quantity

    def remove_product(self, product: ProductInCart):
        product_in_cart = self.find_product(product)

        if product_in_cart is None:
            return

        try:
            product_in_cart.quantity -= product.quantity
        except ValueError:
            product_in_cart.quantity = Quantity(0)
        finally:
            if product_in_cart.quantity == 0:
                self.products.remove(product_in_cart)

    def find_product(self, product_to_find: ProductInCart) -> ProductInCart | None:
        try:
            return next((product_in_cart for product_in_cart in self.products if product_in_cart.product == product_to_find.product))
        except StopIteration:
            return None

    def __len__(self) -> int:
        return len(self.products)

class Cart:
    id: str
    modified_at: datetime
    created_at: datetime
    products_in_cart: ProductsInCart
    order_info: OrderInfo | None
    cart_state: CartState

    def add_product_to_cart(self, product: ProductInCart):
        self.products_in_cart.add_product(product)
    
    def remove_product_from_cart(self, product: ProductInCart):
        self.products_in_cart.remove_product(product)

    def set_order_info(self, order_info: OrderInfo):
        self.order_info = order_info

    def execute_order(self):
        if self.cart_state is not CartState.CREATED:
            raise NotImplementedError()

        if self.order_info is None:
            raise NotImplementedError() 
        
        if not len(self.products_in_cart):
            raise NotImplementedError()


        self.cart_state = CartState.EXECUTED