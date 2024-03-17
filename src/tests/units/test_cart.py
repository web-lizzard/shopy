import pytest
from shop.cart.domain import Cart, CartState, ProductInCart, ProductsInCart, OrderInfo
from shop.cart.exceptions import CartNotReadyError
from shop.product.domain import Product, Money, Quantity

@pytest.fixture
def empty_cart():
    return Cart()

@pytest.fixture
def filled_cart():
    products = ProductsInCart()
    product = Product(name="Product1", price=Money(10), quantity=Quantity(1))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(1))
    products.add_product(product_in_cart)

    order_info = OrderInfo(email='email@email.com', customer_name="John Doe", shipping_address="123 Main St")

    return Cart(products_in_cart=products, order_info=order_info)

def test_create_cart():
    cart = Cart()
    assert cart.id is not None
    assert cart.modified_at is not None
    assert cart.created_at is not None
    assert cart.cart_state == CartState.CREATED
    assert cart.order_info is None

def test_add_product_to_cart(empty_cart):
    product = Product(name="Product1", price=Money(10), quantity=Quantity(1))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(1))

    empty_cart.add_product_to_cart(product_in_cart)
    assert len(empty_cart.products_in_cart.products) == 1

def test_remove_product_from_cart(filled_cart):
    product = Product(name="Product1", price=Money(10), quantity=Quantity(1))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(1))

    filled_cart.remove_product_from_cart(product_in_cart)
    assert len(filled_cart.products_in_cart.products) == 0

def test_set_order_info(empty_cart):
    order_info = OrderInfo(email='email@email.com', customer_name="John Doe", shipping_address="123 Main St")

    empty_cart.set_order_info(order_info)
    assert empty_cart.order_info == order_info

def test_execute_order(empty_cart):
    with pytest.raises(CartNotReadyError):
        empty_cart.execute_order()

    order_info = OrderInfo(customer_name="John Doe", shipping_address="123 Main St", email='test@email.com')
    empty_cart.set_order_info(order_info)

    with pytest.raises(CartNotReadyError):
        empty_cart.execute_order()

    product = Product(name="Product1", price=Money(10), quantity=Quantity(1))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(1))
    empty_cart.add_product_to_cart(product_in_cart)

    empty_cart.execute_order()
    assert empty_cart.cart_state == CartState.EXECUTED