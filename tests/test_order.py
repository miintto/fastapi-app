import pytest

from .test_auth import test_회원가입
from .test_product import test_상품_조회


@pytest.mark.asyncio
async def test_주문_요청(client, create_products):
    product = await test_상품_조회(client, create_products)
    auth = await test_회원가입(client)
    client.headers = {"Authorization": f"JWT {auth["token"]}"}

    data = {
        "order_number": "test",
        "product_id": product["pk"],
        "items": [
            {"item_id": product["items"][0]["pk"], "quantity": 3},
            {"item_id": product["items"][1]["pk"], "quantity": 2},
        ],
    }
    response = await client.post("/orders", json=data)
    assert response.status_code == 200
    return response.json()


@pytest.mark.asyncio
async def test_재고_없이_주문시_실패(client, create_products):
    product = await test_상품_조회(client, create_products)
    auth = await test_회원가입(client)
    client.headers = {"Authorization": f"JWT {auth["token"]}"}

    data = {
        "order_number": "test",
        "product_id": product["pk"],
        "items": [
            {"item_id": product["items"][0]["pk"], "quantity": 0},
            {"item_id": product["items"][1]["pk"], "quantity": 2},
        ],
    }
    response = await client.post("/orders", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_품목_없이_주문시_실패(client, create_products):
    product = await test_상품_조회(client, create_products)
    auth = await test_회원가입(client)
    client.headers = {"Authorization": f"JWT {auth["token"]}"}

    data = {"order_number": "test", "product_id": product["pk"], "items": []}
    response = await client.post("/orders", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_동일한_주문번호로_주문시_실패(client, create_products):
    product = await test_주문_요청(client, create_products)

    data = {
        "order_number": "test",
        "product_id": product["pk"],
        "items": [
            {"item_id": product["items"][0]["pk"], "quantity": 1},
            {"item_id": product["items"][1]["pk"], "quantity": 1},
        ],
    }
    response = await client.post("/orders",  json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_주문_조회(client, create_products):
    order = await test_주문_요청(client, create_products)

    response = await client.get(f"/orders/{order["pk"]}")
    assert response.status_code == 200
