from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.tasks import TaskNotFoundException


async def task_not_found_exception_handler(
        request: Request, exc: TaskNotFoundException
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": exc.message})
