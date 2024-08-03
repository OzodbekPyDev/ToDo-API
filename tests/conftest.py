import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncEngine

from app.main import create_app
from app.infrastructure.di.providers import create_async_container
from dishka.integrations.fastapi import setup_dishka
from app.infrastructure.db.models.sqlalchemy_orm import Base


@pytest_asyncio.fixture(scope="session")
async def container():
    container = create_async_container(db_url="sqlite+aiosqlite:///:memory:")
    engine = await container.get(AsyncEngine)
    # migration
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield container
    await container.close()


@pytest_asyncio.fixture
async def client(container):
    app = create_app()
    setup_dishka(container, app)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient):

    # Login user
    login_response = await client.post("/api/v1/auth/login", data={
        "username": "testuser@mail.ru",
        "password": "testpassword"
    })

    assert login_response.status_code == status.HTTP_200_OK
    client.cookies = login_response.cookies

    yield client
