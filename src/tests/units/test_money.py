import pytest
from shop.product.value_objects import Money

def test_repr():
    money = Money(10000, "USD")
    assert repr(money) == "100.00 USD"

def test_addition():
    money1 = Money(10000, "USD")
    money2 = Money(5000, "USD")
    result = money1 + money2
    assert result.amount == 15000
    assert result.currency == "USD"

def test_subtraction():
    money1 = Money(10000, "USD")
    money2 = Money(5000, "USD")
    result = money1 - money2
    assert result.amount == 5000
    assert result.currency == "USD"

def test_multiplication():
    money = Money(10000, "USD")
    result = money * 2
    assert result.amount == 20000
    assert result.currency == "USD"

def test_division():
    money = Money(10000, "USD")
    result = money / 2
    assert result.amount == 5000
    assert result.currency == "USD"

def test_mint_from_float():
    money = Money.mint(100.0, "USD")
    assert money.amount == 10000
    assert money.currency == "USD"


def test_invalid_currency_addition():
    money1 = Money(10000, "USD")
    money2 = Money(5000, "EUR")
    with pytest.raises(ValueError):
        money1 + money2

def test_invalid_currency_subtraction():
    money1 = Money(10000, "USD")
    money2 = Money(5000, "EUR")
    with pytest.raises(ValueError):
        money1 - money2