from shop.product.domain import Product, Quantity, Money
from shop.cart.domain import ProductInCart, ProductsInCart
import pytest

@pytest.fixture
def empty_cart():
    return ProductsInCart()

@pytest.fixture
def filled_cart():
    product1 = Product(name="Product1", price=Money(10), quantity=Quantity(1))
    product2 = Product(name="Product2", price=Money(20), quantity=Quantity(2))
    product3 = Product(name="Product3", price=Money(30), quantity=Quantity(3))

    product_in_cart1 = ProductInCart(product=product1, quantity=Quantity(1))
    product_in_cart2 = ProductInCart(product=product2, quantity=Quantity(2))
    product_in_cart3 = ProductInCart(product=product3, quantity=Quantity(3))

    cart = ProductsInCart()
    cart.add_product(product_in_cart1)
    cart.add_product(product_in_cart2)
    cart.add_product(product_in_cart3)

    return cart

def test_total_cost_empty_cart(empty_cart):
    assert empty_cart.total_cost == Money(0)

def test_total_cost_filled_cart(filled_cart):
    assert filled_cart.total_cost == Money(140)

def test_add_product(empty_cart):
    product = Product(name="Product1", price=Money(10), quantity=Quantity(1))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(1))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(1))

    empty_cart.add_product(product_in_cart)
    empty_cart.add_product(product_in_cart)
    
    assert len(empty_cart.products) == 1
    assert empty_cart.total_cost == Money(20)

def test_remove_product(filled_cart):
    product = Product(name="Product1", price=Money(10), quantity=Quantity(1))
    product2 = Product(name="Product2", price=Money(20), quantity=Quantity(2))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(1))
    product_in_cart2 = ProductInCart(product=product2, quantity=Quantity(1))

    filled_cart.remove_product(product_in_cart)
    filled_cart.remove_product(product_in_cart2)
    
    assert len(filled_cart.products) == 2
    assert filled_cart.total_cost == Money(110)

def test_find_product(filled_cart):
    product = Product(name="Product2", price=Money(20), quantity=Quantity(2))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(2))

    found_product =  filled_cart.find_product(product_in_cart) 

    assert found_product is not None

def test_find_product_returns_null_product_is_not_in_cart(empty_cart):
    product = Product(name="Product2", price=Money(20), quantity=Quantity(2))
    product_in_cart = ProductInCart(product=product, quantity=Quantity(2))

    found_product = empty_cart.find_product(product_in_cart)

    assert found_product is None