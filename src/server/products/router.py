from fastapi import APIRouter, HTTPException, status
from shop.product.domain import Product, Currency
from shop.product.use_cases import GetProductsUseCase, GetProductUseCase
from shop.product.exceptions import OutOfStockError, ProductNotExistError
from shop.product.dto import GetProductDto, GetProductsDto
from .dependencies import UnitOfWork
from .schemas import ProductSchema
from .utils import convert_product_to_schema

router = APIRouter(prefix="/products")


@router.get("/")
async def get_products(unit_of_work: UnitOfWork) -> list[ProductSchema]:
    dto = GetProductsDto()
    use_case = GetProductsUseCase(unit_of_work)
    products = await use_case.execute(dto)
    return [convert_product_to_schema(product) for product in products]


@router.get("/{product_id}")
async def get_product(product_id: str, unit_of_work: UnitOfWork) -> ProductSchema:
    dto = GetProductDto(id=product_id)
    use_case = GetProductUseCase(unit_of_work)
    try:
        product = await use_case.execute(dto)
        return convert_product_to_schema(product)
    except ProductNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
