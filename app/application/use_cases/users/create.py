from app.application.protocols.interactor import Interactor

# dto
from app.application.dto.users import (
    CreateUserRequest,
    UserResponse
)

# entities
from app.domain.entities.users import UserEntity

# value objects
from app.domain.value_objects.id import IdVO

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.adapters.password_hasher import PasswordHasher

# exceptions
from app.domain.exceptions.users import UserAlreadyExistsException


class CreateUser(Interactor[CreateUserRequest, UserResponse]):

    def __init__(
            self,
            uow: UnitOfWork,
            users_repository: UsersRepository,
            id_provider: IdProvider,
            password_hasher: PasswordHasher
    ) -> None:
        self.uow = uow
        self.users_repository = users_repository
        self.id_provider = id_provider
        self.password_hasher = password_hasher

    async def __call__(self, request: CreateUserRequest) -> UserResponse:
        user_exists = await self.users_repository.get_by_email(email=request.email)
        if user_exists:
            raise UserAlreadyExistsException("User with this email already exists. Please use a different email address")

        user_entity = UserEntity(
            id=IdVO(self.id_provider.generate_uuid()),
            email=request.email,
            password=self.password_hasher.hash_password(request.password)
        )

        await self.users_repository.create(entity=user_entity)
        await self.uow.commit()

        return UserResponse.from_entity(entity=user_entity)
