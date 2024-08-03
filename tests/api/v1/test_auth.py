import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi import status

from app.main import app


@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json={
            "email": "testuser@mail.ru",
            "password": "testpassword"
        })
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/login", data={
            "username": "testuser@mail.ru",
            "password": "testpassword"
        })
    assert response.status_code == status.HTTP_200_OK
