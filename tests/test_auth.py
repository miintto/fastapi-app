import pytest


@pytest.mark.asyncio
async def test_회원가입(client):
    data = {
        "email": "test-user@test.com",
        "password": "password",
        "password_check": "password",
    }
    response = await client.post("/auth/register", json=data)
    assert response.status_code == 200
    return response.json()


@pytest.mark.asyncio
async def test_회원가입_비밀번호_불일치(client):
    data = {
        "email": "test-user@test.com",
        "password": "password",
        "password_check": "1234",
    }
    response = await client.post("/auth/register", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_로그인(client):
    await test_회원가입(client)

    data = {"email": "test-user@test.com", "password": "password"}
    response = await client.post("/auth/login", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_로그인_실패(client):
    await test_회원가입(client)

    data = {"email": "test-user@test.com", "password": "1234"}
    response = await client.post("/auth/login", json=data)
    assert response.status_code == 400
