import pytest

from shop.product.value_objects import Quantity

def test_quantity_representation():
    quantity = Quantity(5)
    assert repr(quantity) == "Quantity(5)"

def test_quantity_equality():
    quantity1 = Quantity(5)
    quantity2 = Quantity(5)
    assert quantity1 == quantity2

def test_quantity_inequality():
    quantity1 = Quantity(5)
    quantity2 = Quantity(3)
    assert quantity1 != quantity2

def test_quantity_subtraction():
    quantity1 = Quantity(5)
    quantity2 = Quantity(3)
    assert quantity1 - quantity2 == Quantity(2)
    assert quantity1 - 2 == Quantity(3)

def test_quantity_multiplication():
    quantity = Quantity(5)
    assert quantity * 2 == Quantity(10)

def test_quantity_division():
    quantity = Quantity(10)
    assert quantity / 2 == Quantity(5)
    with pytest.raises(ValueError):
        quantity / 0

def test_quantity_negative_value():
    with pytest.raises(ValueError):
        Quantity(-5)
