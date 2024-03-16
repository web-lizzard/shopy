from fastapi import APIRouter
from shop.product.domain import Product, Currency
from shop.product.use_cases import GetProductsUseCase, GetProductUseCase
from shop.product.exceptions import OutOfStockError, ProductNotExistError
from shop.product.dto import GetProductDto, GetProductsDto
from .dependencies import UnitOfWork
from .schemas import ProductSchema
from .utils import convert_product_to_schema

router = APIRouter(prefix='/products')


@router.get('/')
async def get_products(unit_of_work: UnitOfWork) -> list[ProductSchema]:
    dto = GetProductsDto()
    use_case = GetProductsUseCase(unit_of_work)
    products = await use_case.execute(dto)
    return [convert_product_to_schema(product) for product in products]