from app.application.protocols.interactor import Interactor

# dto
from app.application.dto.users import (
    UserResponse
)

# repositories [domain]
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# exceptions
from app.domain.exceptions.users import UserNotFoundException


class GetAllUsers(Interactor[None, list[UserResponse]]):

    def __init__(
            self,
            users_repository: UsersRepository
    ) -> None:
        self.users_repository = users_repository

    async def __call__(self, request: None = None) -> list[UserResponse]:
        user_entities = await self.users_repository.get_all()

        return [UserResponse.from_entity(user_entity) for user_entity in user_entities]


class GetCurrentUser(Interactor[None, UserResponse]):

    def __init__(
            self,
            users_repository: UsersRepository,
            jwt_processor: JwtTokenProcessor,
    ) -> None:
        self.users_repository = users_repository
        self.jwt_processor = jwt_processor

    async def __call__(self, request: None = None) -> UserResponse:
        user_id = self.jwt_processor.get_current_user_id()

        user_entity = await self.users_repository.get_by_id(id=user_id)

        if not user_entity:
            raise UserNotFoundException("User not found, something went wrong")

        return UserResponse.from_entity(entity=user_entity)
