from shop.product.exceptions import ProductNotExistError
from shop.product.infrastructure import ProductRepository, ProductUnitOfWork
from shop.product.domain import Product


class FakeRepository(ProductRepository):
    def __init__(self, products: list[Product] | None = None):
        self.products = products if products else []

    async def get(self, id: str):
        for product in self.products:
            if product.id == id:
                return product
        return None

    async def list(self, limit: int, skip: int):
        return self.products[skip : skip + limit]

    async def update_quantity(self, product_to_change: Product) -> Product:
        for idx, product in enumerate(self.products):
            if product.id == product_to_change.id:
                self.products[idx] = product_to_change
                return product_to_change
        raise ValueError("Product not found")


class FakeUnitOfWork(ProductUnitOfWork):
    repository = FakeRepository()

    def __init__(self, products: list[Product] | None = None) -> None:
        self.repository = FakeRepository(products)
        self.committed = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass
