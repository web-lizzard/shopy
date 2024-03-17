from dataclasses import dataclass, field

from .value_objects import Quantity, Money, ProductQuantityActions
from datetime import datetime
import uuid

@dataclass
class Product:
    quantity: Quantity
    price: Money
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str | None = None
    image_url: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)

    def change_quantity(self, value: int, action: ProductQuantityActions):
        match action:
            case ProductQuantityActions.ADD:
                self.add_quantity(value)
            case ProductQuantityActions.SUBTRACT:
                self.subtract_quantity(value)

    def add_quantity(self, value: int):
        self.quantity = self.quantity + value
    
    def subtract_quantity(self, value: int):
        self.quantity = self.quantity - value

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Product):
            return __value.name == self.name
        
        return False
