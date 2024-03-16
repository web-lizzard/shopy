

class ProductNotExistError(Exception):
    def __init__(self, product_id: str) -> None:
        super().__init__(f'{product_id} not exist')


class OutOfStockError(Exception):
    def __init__(self, product_name: str) -> None:
        super().__init__(f"Out of stock of product: {product_name}")