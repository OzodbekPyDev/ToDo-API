import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi import status

from app.main import app


@pytest.fixture
async def get_cookies():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        # Login user
        login_response = await ac.post("/api/v1/auth/login", data={
            "username": "testuser@mail.ru",
            "password": "testpassword"
        })
        assert login_response.status_code == status.HTTP_200_OK

        return ac.cookies
