import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine

from core.db.model import Base
from shop.cart.domain import CartState
from shop.models import Product, OrderInfo, Cart, ProductInCart
from datetime import datetime, timedelta

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

@pytest.fixture(scope='function')
async def cart_model(session_factory):
    async with session_factory() as session:
        cart = Cart(expired_at = datetime.now() + timedelta(minutes=10), cart_state=CartState.CREATED)
        session.add(cart)
        await session.commit()
        yield cart
        session.delete(cart)
        await session.commit()

@pytest.fixture(scope='function')
async def product_in_cart_model(session_factory, product_model, cart_model):
    async with session_factory as session:
        product = ProductInCart(product_id=product_model.id, cart_id=cart_model.id)
        session.add(product)
        await session.commit()
        yield product
        session.delete(product)
        await session.commit()


@pytest.fixture(scope='function')
async def order_info_model(session_factory, cart_model):
    async with session_factory() as session:
        order_info = OrderInfo(cart_id=cart_model.id, shipping_address='address', customer_name='name', email='test@email.com')
        session.add(order_info)
        await session.commit()
        yield order_info
        session.delete(order_info)
        await session.commit()