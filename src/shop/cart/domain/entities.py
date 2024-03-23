from dataclasses import dataclass, field
from datetime import datetime, timedelta
import functools
from uuid import uuid4

from shop.product.domain import Quantity , Money
from .value_objects import ProductInCart, CartState, OrderInfo
from ..exceptions import CartNotReadyError


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
    expired_at: datetime

    def __init__(self, 
                 id: str | None = None, 
                 products_in_cart: ProductsInCart | None = None, 
                 modified_at: datetime = datetime.now(), 
                 created_at: datetime = datetime.now(), 
                 cart_state: CartState = CartState.CREATED, 
                 order_info: OrderInfo | None = None,
                 expired_at: datetime = datetime.now() + timedelta(hours=2)
                 ) -> None:
        
        
        self.id = id if id else str(uuid4())
        self.products_in_cart = products_in_cart if products_in_cart else ProductsInCart()
        self.cart_state = cart_state
        self.order_info = order_info
        self.modified_at = modified_at
        self.created_at = created_at
        self.expired_at = expired_at

    def add_product_to_cart(self, product: ProductInCart):
        self.products_in_cart.add_product(product)
    
    def remove_product_from_cart(self, product: ProductInCart):
        self.products_in_cart.remove_product(product)

    def set_order_info(self, order_info: OrderInfo):
        self.order_info = order_info

    def execute_order(self):
        if self.cart_state is not CartState.CREATED:
            raise CartNotReadyError(self.cart_state)

        if self.order_info is None:
            raise CartNotReadyError('You have to provide order info')
        
        if not len(self.products_in_cart):
            raise CartNotReadyError("You have to add at least one product to cart")


        self.cart_state = CartState.EXECUTED