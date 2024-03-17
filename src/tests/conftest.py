import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine

from core.db.model import Base
from shop.model import Product

@pytest.fixture(scope='function')
async def engine():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    yield engine
    await engine.dispose()

@pytest.fixture(scope='function', autouse=True)
async def manage_tables(engine: AsyncEngine):
    # Create tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.connect() as connect:
        await connect.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def session_factory(engine):
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    yield async_session
    
    async with async_session() as session:
        await session.rollback()
        await session.close()

@pytest.fixture(scope="function")
async def product_model(session_factory):
    async with session_factory() as session:
        product = Product(name="Test Product", quantity=10, price=10000)
        session.add(product)
        await session.commit()
        yield product
        session.delete(product)
        await session.commit()