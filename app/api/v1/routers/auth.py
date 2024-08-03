from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from dishka.integrations.fastapi import DishkaRoute, FromDishka

# dto
from app.application.dto.users import (
    CreateUserRequest,
    LoginUserRequest,
    UserResponse
)

# use cases
from app.application.use_cases.users.create import CreateUser
from app.application.use_cases.users.login import LoginUser
from app.application.use_cases.users.get import GetCurrentUser

# adapters [domain]
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# value objects
from app.domain.value_objects.id import IdVO

# dependencies
from app.api.v1.routers.dependencies.auth import auth_required

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    route_class=DishkaRoute
)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(
        request: CreateUserRequest,
        create_user_interactor: FromDishka[CreateUser]
) -> UserResponse:
    return await create_user_interactor(request)


@router.post('/login')
async def login(
        response: Response,
        login_request: Annotated[OAuth2PasswordRequestForm, Depends()],
        login_user_interactor: FromDishka[LoginUser],
        token_processor: FromDishka[JwtTokenProcessor]
) -> UserResponse:
    request = LoginUserRequest(
        email=login_request.username,
        password=login_request.password
    )
    user = await login_user_interactor(request)
    token = token_processor.generate_token(user_id=IdVO(user.id))
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True
    )

    return user


@router.get('/me', dependencies=[Depends(auth_required)])
async def get_current_user(
        current_user_interactor: FromDishka[GetCurrentUser]
) -> UserResponse:
    return await current_user_interactor()
