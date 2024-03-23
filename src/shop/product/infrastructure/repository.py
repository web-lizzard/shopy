import abc

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..domain import Product, Quantity, Money
from ...models import Product as ProductModel
from ..exceptions import ProductNotExistError




class ProductBuilder:
    def __init__(self, model: ProductModel) -> None:
        self._model = model

    def build(self) -> Product:
        return Product(quantity=Quantity(self._model.quantity), 
                       price=Money(self._model.price), 
                       name= self._model.name,
                       id=self._model.id, 
                       description=self._model.description, 
                       image_url=self._model.description, 
                       created_at=self._model.created_at, 
                       modified_at=self._model.modified_at
                       )


class ProductRepository(abc.ABC):

    @abc.abstractmethod
    async def get(self, id: str) -> Product | None:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def list(self, limit: int, skip: int) -> list[Product]:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def update_quantity(self, product_to_change: Product) -> Product:
        raise NotImplementedError
    


class SQLProductRepository(ProductRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, id: str) -> Product | None:
        product = await self._get(id)
        return ProductBuilder(product).build() if product else None
    
    async def update_quantity(self, product_to_change: Product) -> Product:
        db_product = await self._get(product_to_change.id)

        if db_product is None:
            raise ProductNotExistError(product_id=product_to_change.id)
        
        db_product.quantity = product_to_change.quantity.value

        return ProductBuilder(db_product).build()
    
    async def list(self, limit: int = 5, skip: int = 0) -> list[Product]:
        statement = select(ProductModel).offset(skip).limit(limit)
        products = await self._session.scalars(statement)

        return [ProductBuilder(product).build() for product in products]

    async def _get(self, id: str) -> ProductModel | None:
        statement = select(ProductModel).filter_by(id=id)
        product = await self._session.scalar(statement)
        return product



