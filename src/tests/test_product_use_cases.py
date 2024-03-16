import pytest
from .mocks import FakeUnitOfWork
from shop.product.dto import GetProductDto, GetProductsDto, UpdateProductQuantityDto
from shop.product.use_cases import UpdateProductQuantityUseCase, GetProductUseCase, GetProductsUseCase
from shop.product.domain import Product, Quantity, Money, ProductQuantityActions
from shop.product.exceptions import OutOfStockError


@pytest.fixture
def product():
    return Product(price=Money.mint(35.5), quantity=Quantity(5), name='test')

@pytest.fixture
def unit_of_work(product):
    products = [product]
    return FakeUnitOfWork(products=products)


async def test_get_products_use_cases_returns_list(unit_of_work):
    use_case = GetProductsUseCase(unit_of_work)
    dto = GetProductsDto()
    
    products = await use_case.execute(dto)

    assert len(products) == 1

async def test_get_product_use_case_return_product(unit_of_work, product):
    use_case = GetProductUseCase(unit_of_work=unit_of_work)
    dto = GetProductDto(id=product.id)

    product = await use_case.execute(dto)

    assert product is not None
    assert isinstance(product, Product)


async def test_update_product_use_case_update_quantity(unit_of_work, product):
    use_case = UpdateProductQuantityUseCase(unit_of_work)
    dto = UpdateProductQuantityDto(id=product.id, action=ProductQuantityActions.ADD, amount=15)

    product = await use_case.execute(dto)

    assert product.quantity == 20
    assert unit_of_work.committed is True


async def test_update_product_use_case_raises_error_when_quantity_is_less_than_zero(unit_of_work, product):
    use_case = UpdateProductQuantityUseCase(unit_of_work)
    dto = UpdateProductQuantityDto(id=product.id, action=ProductQuantityActions.SUBTRACT, amount=45)

    with pytest.raises(OutOfStockError) as e:
        await use_case.execute(dto)
        
        assert str(e) == f'Out of stock of product: {product.name}'
