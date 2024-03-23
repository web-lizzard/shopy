from shop.models import Product as ProductModel
from shop.product.domain import Product, Quantity, Money
from shop.product.infrastructure.repository import SQLProductRepository, ProductBuilder

async def test_get_product_returns_product_domain_object(session_factory, product_model):
    async with session_factory() as session:
        repo = SQLProductRepository(session)

        product = await repo.get(id=product_model.id)

        assert product is not None
        assert isinstance(product, Product)

async def test_list_returns_products(session_factory, product_model):
    async with session_factory() as session:
        repo = SQLProductRepository(session)

        products = await repo.list()

        assert len(products) == 1

async def test_update_quantity_updates_q_correctly(session_factory, product_model):
    async with session_factory() as session:
        repo = SQLProductRepository(session)
        product_to_update = ProductBuilder(product_model).build()
        product_to_update.add_quantity(10)
        updated_product = await repo.update_quantity(product_to_update)

        await session.commit()

        p = await repo.get(updated_product.id)

        assert p is not None
        assert p.quantity == 20

