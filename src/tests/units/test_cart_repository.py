from shop.cart.infrastracture.repository import SQLCartRepository, CartUpdateAction
from shop.cart.domain import Cart, ProductInCart, OrderInfo
from shop.product.infrastructure import ProductBuilder
from shop.product.domain import Quantity, Money


async def test_get_cart(session_factory, cart_model):
    async with session_factory() as session:
        repo = SQLCartRepository(session=session)

        cart = await repo.get(cart_model.id)

        assert cart is not None
        assert isinstance(cart, Cart)


async def test_create_cart(session_factory):
    async with session_factory() as session:
        repo = SQLCartRepository(session=session)

        cart = await repo.create()
        await session.commit()

        assert cart is not None
        assert isinstance(cart, Cart)


async def test_update_cart_add_item(session_factory, cart_model, product_model):
    async with session_factory() as session:
        repo = SQLCartRepository(session=session)
        cart = await repo.get(cart_model.id)
        assert cart is not None
        initial_modified = cart.modified_at

        cart.add_product_to_cart(
            ProductInCart(
                product=ProductBuilder(product_model).build(),
                quantity=Quantity(product_model.quantity),
            )
        )

        await repo.update(cart, [CartUpdateAction.UPDATE_CART_ITEMS])
        await session.commit()

        updated_cart = await repo.get(cart_model.id)

        assert updated_cart is not None

        assert len(updated_cart.products_in_cart) == 1
        assert updated_cart.products_in_cart.total_cost == Money(10000 * 10)
        assert initial_modified != updated_cart.modified_at


async def test_update_cart_set_order_info(session_factory, cart_model):
    async with session_factory() as session:
        repo = SQLCartRepository(session)

        cart = await repo.get(cart_model.id)

        assert cart is not None

        cart.set_order_info(
            order_info=OrderInfo(
                email="test@email.com", shipping_address="address", customer_name="name"
            )
        )

        await repo.update(cart, [CartUpdateAction.UPDATE_ORDER_INFO])

        await session.commit()
        cart = await repo.get(cart_model.id)

        assert cart is not None

        assert cart.order_info is not None
        assert cart.order_info.email is "test@email.com"
