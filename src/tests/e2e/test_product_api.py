import pytest
from fastapi import status
from server.products.utils import convert_product_to_schema
from shop.product.infrastructure import ProductBuilder

@pytest.fixture
def expected_response(product_model):
    return convert_product_to_schema(ProductBuilder(product_model).build()).model_dump()

async def test_get_products_returns_list(client, session_maker_override, product_model): 
    response =  client.get('/products')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


async def test_get_product_returns_product(client, session_maker_override, product_model, expected_response):
    response = client.get('/products/'+ product_model.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response