from app.application.protocols.interactor import Interactor

# dto
from app.application.dto.users import (
    LoginUserRequest,
    UserResponse
)

# repositories [domain]
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.password_hasher import PasswordHasher

# exceptions
from app.domain.exceptions.users import InvalidAuthCredentialsException


class LoginUser(Interactor[LoginUserRequest, UserResponse]):

    def __init__(
            self,
            users_repository: UsersRepository,
            password_hasher: PasswordHasher
    ) -> None:
        self.users_repository = users_repository
        self.password_hasher = password_hasher

    async def __call__(self, request: LoginUserRequest) -> UserResponse:
        user_entity = await self.users_repository.get_by_email(email=request.email)

        if not user_entity:
            raise InvalidAuthCredentialsException("Invalid credentials. Please check your email and password and try again.")

        is_correct_password = self.password_hasher.verify_password(
            password=request.password, hashed_password=user_entity.password
        )

        if not user_entity or not is_correct_password:
            raise InvalidAuthCredentialsException("Invalid credentials. Please check your email and password and try again.")

        return UserResponse.from_entity(entity=user_entity)
