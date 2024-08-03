from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import include_all_routers
from app.infrastructure.exception_handlers import init_exception_handlers
from app.infrastructure.di.providers import container


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


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
setup_dishka(container, app)
