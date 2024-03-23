import abc

from ..domain import Product
from ..dto import GetProductDto, GetProductsDto, UpdateProductQuantityDto
from ..exceptions import ProductNotExistError, OutOfStockError
from ..infrastructure.uow import ProductUnitOfWork


class ProductUseCase(abc.ABC):
    def __init__(self, unit_of_work: ProductUnitOfWork) -> None:
        self.uow = unit_of_work

    @abc.abstractmethod
    async def execute(self):
        raise NotImplementedError


class GetProductsUseCase(ProductUseCase):
    async def execute(self, dto: GetProductsDto) -> list[Product]:
        async with self.uow:
            products = await self.uow.repository.list(limit=dto.limit, skip=dto.skip)

            return products


class GetProductUseCase(ProductUseCase):
    async def execute(self, dto: GetProductDto) -> Product:
        async with self.uow:
            product = await self.uow.repository.get(dto.id)

            if product is None:
                raise ProductNotExistError(product_id=dto.id)

            return product


class UpdateProductQuantityUseCase(ProductUseCase):
    async def execute(self, dto: UpdateProductQuantityDto) -> Product:
        async with self.uow:
            product_to_update = await self.uow.repository.get(dto.id)

            if product_to_update is None:
                raise ProductNotExistError(product_id=dto.id)
            try:
                product_to_update.change_quantity(value=dto.amount, action=dto.action)
            except ValueError:
                raise OutOfStockError(product_name=product_to_update.name)
            else:
                updated_product = await self.uow.repository.update_quantity(
                    product_to_update
                )
                await self.uow.commit()
                return updated_product
