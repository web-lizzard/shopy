import pytest
from shop.product.value_objects import Quantity

def test_repr():
    quantity = Quantity(5)
    assert repr(quantity) == "Quantity(5)"

def test_equality():
    quantity1 = Quantity(5)
    quantity2 = Quantity(5)
    assert quantity1 == quantity2

def test_inequality():
    quantity1 = Quantity(5)
    quantity2 = Quantity(3)
    assert quantity1 != quantity2

def test_greater_than():
    quantity1 = Quantity(5)
    quantity2 = Quantity(3)
    assert quantity1 > quantity2

def test_less_than():
    quantity1 = Quantity(3)
    quantity2 = Quantity(5)
    assert quantity1 < quantity2

def test_greater_than_or_equal():
    quantity1 = Quantity(5)
    quantity2 = Quantity(5)
    quantity3 = Quantity(3)
    assert quantity1 >= quantity2
    assert quantity1 >= quantity3

def test_less_than_or_equal():
    quantity1 = Quantity(3)
    quantity2 = Quantity(5)
    quantity3 = Quantity(3)
    assert quantity1 <= quantity2
    assert quantity1 <= quantity3

def test_comparison_with_int():
    quantity = Quantity(5)
    assert quantity == 5
    assert quantity > 3
    assert quantity < 10

def test_negative_quantity():
    with pytest.raises(ValueError):
        Quantity(-5)
