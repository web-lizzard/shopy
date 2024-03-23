import abc
from ..domain import OrderInfo, Cart, ProductInCart, ProductsInCart, CartState
from shop.product.domain import Money, Product, Quantity
from ...models import OrderInfo as OrderInfoModel, ProductInCart as ProductInCartModel, Cart as CartModel, Product as ProductModel
from enum import StrEnum

import functools
from .builders import CartBuilder

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import asdict
from datetime import datetime, timedelta

class CartUpdateAction(StrEnum):
    UPDATE_CART_ITEMS = 'update_card_items'
    UPDATE_ORDER_INFO = 'update_order_info'
    UPDATE_CART_STATE = 'update_cart_state'

class CartRepository(abc.ABC):

    @abc.abstractmethod
    async def get(self, id: str) -> Cart | None:
        raise NotImplementedError
        
    @abc.abstractmethod    
    async def update(self, cart_to_update: Cart) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def create(self) -> Cart:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def update_order_info(self, cart: Cart) -> str:
        raise NotImplementedError
    

class SQLCartRepository(CartRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: str) -> Cart | None:
        cart_model = await self._get(id=id)

        return CartBuilder(cart_model).build() if cart_model else None
    
    async def create(self) -> Cart:
        model = CartModel(expired_at=datetime.now() + timedelta(hours=1), cart_state=CartState.CREATED)
        self.session.add(model)
        return CartBuilder(model).build()
    
    async def update(self, cart: Cart, actions: list[CartUpdateAction]):
        cart_model =  await self._get(cart.id)
        
        if CartUpdateAction.UPDATE_CART_ITEMS in actions:
            self.update_cart_items(cart, cart_model)
        if CartUpdateAction.UPDATE_ORDER_INFO in actions:
            self.update_order_info(cart, cart_model)
        if CartUpdateAction.UPDATE_CART_STATE in actions:
            cart_model.cart_state = cart.cart_state

        cart_model.modified_at = datetime.now()

    
    def update_order_info(self, cart: Cart, model: CartModel):
        if cart.order_info is None:
            raise NotImplementedError

        model.order_info = OrderInfoModel(cart_id=cart.id, **asdict(cart.order_info))
    
    def update_cart_items(self, cart_to_update: Cart, model: CartModel):
        model.products_in_cart = [ProductInCartModel(product_id=p.product.id, cart_id=model.id, quantity=p.quantity.value) for p in cart_to_update.products_in_cart.products]

    async def _get(self, id: str) -> CartModel:
        statement = select(CartModel).filter_by(id=id).options(joinedload(CartModel.products_in_cart).subqueryload(ProductInCartModel.product), joinedload(CartModel.order_info))
        cart = await self.session.scalar(statement)

        if cart is None:
            raise NotImplementedError

        return cart
    
