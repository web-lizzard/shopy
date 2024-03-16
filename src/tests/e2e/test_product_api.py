from fastapi import status

async def test_get_products_returns_list(client, session_maker_override, product_model): 
    response =  client.get('/products')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


async def test_get_product_returns_product(client, session_maker_override, product_model):
    response = client.get('/products/'+ product_model.id)

    assert response.status_code == status.HTTP_200_OK