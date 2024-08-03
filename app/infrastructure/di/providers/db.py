import os
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine,)

from app.infrastructure.config import settings


def is_pytest_running():
    try:
        import pytest
        return True
    except ImportError:
        return False


class DBProvider(Provider):

    @provide(scope=Scope.APP)
    async def provide_engine(self) -> AsyncEngine:
        # БД для тестов (pytest)
        if is_pytest_running():
            engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
            from app.infrastructure.db.models.sqlalchemy_orm import Base
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

            return engine
        else:
            return create_async_engine(settings.database_url, echo=settings.ECHO)

    @provide(scope=Scope.APP)
    def provide_session_maker(
        self, engine: FromDishka[AsyncEngine]
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self, session_maker: FromDishka[async_sessionmaker[AsyncSession]]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session
