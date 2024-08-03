from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import include_all_routers
from app.infrastructure.exception_handlers import init_exception_handlers
from app.infrastructure.di.providers import create_async_container
from app.infrastructure.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="ToDo API",
        lifespan=lifespan,
    )
    include_all_routers(app)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_exception_handlers(app)
    return app


def create_production_app() -> FastAPI:
    app = create_app()
    container = create_async_container(db_url=settings.database_url)
    setup_dishka(container, app)
    return app


app = create_production_app()  # to start with uvicorn app.main:app
