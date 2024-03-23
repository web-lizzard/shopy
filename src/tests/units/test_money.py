import pytest
from shop.product.domain import Money, Currency


def test_repr():
    money = Money(10000, Currency.USD)
    assert repr(money) == "100.00 USD"


def test_addition():
    money1 = Money(10000)
    money2 = Money(5000)
    result = money1 + money2
    assert result.amount == 15000
    assert result.currency == "USD"


def test_subtraction():
    money1 = Money(10000)
    money2 = Money(5000)
    result = money1 - money2
    assert result.amount == 5000
    assert result.currency == "USD"


def test_multiplication():
    money = Money(10000)
    result = money * 2
    assert result.amount == 20000
    assert result.currency == "USD"


def test_division():
    money = Money(10000)
    result = money / 2
    assert result.amount == 5000
    assert result.currency == "USD"


def test_mint_from_float():
    money = Money.mint(100.0, Currency.USD)
    assert money.amount == 10000
    assert money.currency == "USD"


def test_invalid_currency_addition():
    money1 = Money(10000, Currency.EUR)
    money2 = Money(5000, Currency.USD)
    with pytest.raises(ValueError):
        money1 + money2


def test_invalid_currency_subtraction():
    money1 = Money(10000, Currency.USD)
    money2 = Money(5000, Currency.EUR)
    with pytest.raises(ValueError):
        money1 - money2
