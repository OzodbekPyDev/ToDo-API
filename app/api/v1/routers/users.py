from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

# dto
from app.application.dto.users import UserResponse

# use cases
from app.application.use_cases.users.get import GetAllUsers


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    route_class=DishkaRoute,
)


@router.get("/")
async def get_users(
        get_users_interactor: FromDishka[GetAllUsers]
) -> list[UserResponse]:
    return await get_users_interactor()
