from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.users import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidAuthCredentialsException
)


async def user_already_exists_exception_handler(
        request: Request, exc: UserAlreadyExistsException
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"message": exc.message})


async def user_not_found_exception_handler(
        request: Request, exc: UserNotFoundException
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": exc.message})


async def invalid_auth_credentials_exception_handler(
        request: Request, exc: InvalidAuthCredentialsException
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": exc.message})
