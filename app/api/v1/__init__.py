from fastapi import FastAPI

# routers
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.users import router as users_router
from app.api.v1.routers.tasks import router as tasks_router
from app.api.v1.routers.task_permissions import router as task_permissions_router

all_routers = [
    auth_router,
    users_router,
    tasks_router,
    task_permissions_router,
]


def include_all_routers(app: FastAPI) -> None:
    for router in all_routers:
        app.include_router(router, prefix="/api/v1")
