from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from shop.product.domain import Product, Currency
from shop.product.use_cases import GetProductsUseCase, GetProductUseCase
from shop.product.exceptions import OutOfStockError, ProductNotExistError
from shop.product.dto import GetProductDto, GetProductsDto
from shop.product.infrastructure import ProductUnitOfWork, SQLProductUnitOfWork
from core.db import DEFAULT_SESSION_MAKER


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return DEFAULT_SESSION_MAKER


SessionMaker = Annotated[async_sessionmaker[AsyncSession], Depends(get_sessionmaker)]


def get_unit_of_work(
    session_factory: Annotated[SessionMaker, Depends(get_sessionmaker)]
) -> ProductUnitOfWork:
    return SQLProductUnitOfWork(session_factory)


UnitOfWork = Annotated[ProductUnitOfWork, Depends(get_unit_of_work)]
