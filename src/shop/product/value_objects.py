from dataclasses import dataclass
from decimal import Decimal
from typing import Self

@dataclass
class Money:
    amount: int
    currency: str

    @classmethod
    def mint(cls, value: float | Decimal, currency: str) -> Self:
            amount = int(value * 100)
            return cls(amount=amount, currency=currency)

    def __repr__(self):
        return f"{self.amount / 100:.2f} {self.currency}"

    def __add__(self, other):
        if self.currency == other.currency:
            return Money(self.amount + other.amount, self.currency)
        
        raise ValueError("Cannot add money with different currencies")

    def __sub__(self, other):
        if self.currency == other.currency:
            return Money(self.amount - other.amount, self.currency)
        raise ValueError("Cannot subtract money with different currencies")

    def __mul__(self, other):
        if isinstance(other, int):
            return Money(self.amount * other, self.currency)
        
        raise TypeError("Multiplication is only supported by an integer")

    def __truediv__(self, other):
        if not isinstance(other, int):
            raise TypeError("Division is only supported by an integer")
        
        if other == 0:
            raise ValueError("Division by zero")
    
        return Money(self.amount // other, self.currency)


from dataclasses import dataclass

@dataclass
class Quantity:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Quantity cannot be lower than 0")

    def __repr__(self):
        return f"Quantity({self.value})"

    def __eq__(self, other):
        if isinstance(other, Quantity):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        
        return False

    def __lt__(self, other):
        if isinstance(other, Quantity):
            return self.value < other.value
        if isinstance(other, int):
            return self.value < other
        
        raise TypeError("Unsupported operand type(s) for <: 'Quantity' and '{}'".format(type(other).__name__))

    def __le__(self, other):
        if isinstance(other, Quantity):
            return self.value <= other.value
        if isinstance(other, int):
            return self.value <= other
        
        raise TypeError("Unsupported operand type(s) for <=: 'Quantity' and '{}'".format(type(other).__name__))

    def __gt__(self, other):
        if isinstance(other, Quantity):
            return self.value > other.value
        if isinstance(other, int):
            return self.value > other
        
        raise TypeError("Unsupported operand type(s) for >: 'Quantity' and '{}'".format(type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, Quantity):
            return self.value >= other.value
        if isinstance(other, int):
            return self.value >= other
       
        raise TypeError("Unsupported operand type(s) for >=: 'Quantity' and '{}'".format(type(other).__name__))




