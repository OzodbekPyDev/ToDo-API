import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "testuser@mail.ru",
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):

    response = await client.post("/api/v1/auth/login", data={
        "username": "testuser@mail.ru",
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_200_OK
