from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.task_permissions import (
    PermissionDeniedException,
    TaskPermissionNotFoundException
)


async def permission_denied_exception_handler(
        request: Request, exc: PermissionDeniedException
) -> JSONResponse:
    return JSONResponse(status_code=403, content={"message": exc.message})


async def task_permission_not_found_exception_handler(
        request: Request, exc: TaskPermissionNotFoundException
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": exc.message})
