import abc
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .repository import ProductRepository, SQLProductRepository
from core.db import DEFAULT_SESSION_MAKER


class ProductUnitOfWork(abc.ABC):
    repository: ProductRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abc.abstractmethod
    async def commit():
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback():
        raise NotImplementedError


class SQLProductUnitOfWork(ProductUnitOfWork):
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession] = DEFAULT_SESSION_MAKER
    ) -> None:
        self._session_factory = session_factory
        super().__init__()

    async def __aenter__(self):
        self.session = self._session_factory()
        self.repository = SQLProductRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        return await super().__aexit__(*args)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
