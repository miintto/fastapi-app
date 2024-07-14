import pytest


@pytest.mark.asyncio
async def test_상품_리스트_조회(client, create_products):
    response = await client.get("/products")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_상품_조회(client, create_products):
    product_id = create_products[0]

    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 200
    return response.json()


@pytest.mark.asyncio
async def test_존재하지_않는_상품_조회(client, create_products):
    product_id = create_products[0]

    response = await client.get(f"/products/{product_id + 999}")
    assert response.status_code == 404
