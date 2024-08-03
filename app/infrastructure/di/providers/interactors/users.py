from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka

# use cases
from app.application.use_cases.users.create import CreateUser
from app.application.use_cases.users.login import LoginUser
from app.application.use_cases.users.get import GetCurrentUser, GetAllUsers

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor
from app.domain.protocols.adapters.password_hasher import PasswordHasher


class UsersInteractorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_create(
            self,
            uow: FromDishka[UnitOfWork],
            users_repository: FromDishka[UsersRepository],
            id_provider: FromDishka[IdProvider],
            password_hasher: FromDishka[PasswordHasher]
    ) -> CreateUser:
        return CreateUser(
            uow=uow,
            users_repository=users_repository,
            id_provider=id_provider,
            password_hasher=password_hasher
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_all(
            self,
            users_repository: FromDishka[UsersRepository]
    ) -> GetAllUsers:
        return GetAllUsers(
            users_repository=users_repository
        )

    @provide(scope=Scope.REQUEST)
    def provide_login(
            self,
            users_repository: FromDishka[UsersRepository],
            password_hasher: FromDishka[PasswordHasher]
    ) -> LoginUser:
        return LoginUser(
            users_repository=users_repository,
            password_hasher=password_hasher
        )

    @provide(scope=Scope.REQUEST)
    def provide_me(
            self,
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor]
    ) -> GetCurrentUser:
        return GetCurrentUser(
            users_repository=users_repository,
            jwt_processor=jwt_processor
        )
