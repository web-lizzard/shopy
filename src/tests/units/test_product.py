import pytest

from shop.product.domain import Product, Quantity, Money, ProductQuantityActions

@pytest.fixture
def product():
    return Product(id="1", quantity=Quantity(10), price=Money(2), name='test')

def test_add_quantity(product: Product):
    initial_quantity = product.quantity
    product.add_quantity(5)
    assert product.quantity == initial_quantity + 5

def test_subtract_quantity(product: Product):
    initial_quantity = product.quantity
    product.subtract_quantity(3)
    assert product.quantity == initial_quantity - 3

def test_change_quantity_add(product: Product):
    initial_quantity = product.quantity
    product.change_quantity(7, ProductQuantityActions.ADD)
    assert product.quantity == initial_quantity + 7

def test_change_quantity_subtract(product: Product):
    initial_quantity = product.quantity
    product.change_quantity(4, ProductQuantityActions.SUBTRACT)
    assert product.quantity == initial_quantity - 4