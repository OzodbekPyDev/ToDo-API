from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka

# use cases
from app.application.use_cases.task_permissions.create import CreateTaskPermission
from app.application.use_cases.task_permissions.get import (
    GetAllTaskPermissionsGrantedToUser,
    GetAllTaskPermissionsGrantedToTask
)
from app.application.use_cases.task_permissions.update import UpdateTaskPermission
from app.application.use_cases.task_permissions.delete import DeleteTaskPermission

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor


class TaskPermissionsInteractorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_create(
            self,
            uow: FromDishka[UnitOfWork],
            task_permissions_repository: FromDishka[TaskPermissionsRepository],
            tasks_repository: FromDishka[TasksRepository],
            users_repository: FromDishka[UsersRepository],
            id_provider: FromDishka[IdProvider],
            jwt_processor: FromDishka[JwtTokenProcessor]
    ) -> CreateTaskPermission:
        return CreateTaskPermission(
            uow=uow,
            task_permissions_repository=task_permissions_repository,
            tasks_repository=tasks_repository,
            users_repository=users_repository,
            id_provider=id_provider,
            jwt_processor=jwt_processor,
        )

    @provide(scope=Scope.REQUEST)
    async def provide_get_all_granted_to_user(
            self,
            task_permissions_repository: FromDishka[TaskPermissionsRepository],
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor]
    ) -> GetAllTaskPermissionsGrantedToUser:
        return GetAllTaskPermissionsGrantedToUser(
            task_permissions_repository=task_permissions_repository,
            users_repository=users_repository,
            jwt_processor=jwt_processor
        )

    @provide(scope=Scope.REQUEST)
    async def provide_get_all_granted_to_task(
            self,
            task_permissions_repository: FromDishka[TaskPermissionsRepository],
            tasks_repository: FromDishka[TasksRepository],
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor]
    ) -> GetAllTaskPermissionsGrantedToTask:
        return GetAllTaskPermissionsGrantedToTask(
            task_permissions_repository=task_permissions_repository,
            tasks_repository=tasks_repository,
            users_repository=users_repository,
            jwt_processor=jwt_processor
        )

    @provide(scope=Scope.REQUEST)
    def provide_update(
            self,
            uow: FromDishka[UnitOfWork],
            task_permissions_repository: FromDishka[TaskPermissionsRepository],
            tasks_repository: FromDishka[TasksRepository],
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor]
    ) -> UpdateTaskPermission:
        return UpdateTaskPermission(
            uow=uow,
            task_permissions_repository=task_permissions_repository,
            tasks_repository=tasks_repository,
            users_repository=users_repository,
            jwt_processor=jwt_processor,
        )

    @provide(scope=Scope.REQUEST)
    def provide_delete(
            self,
            uow: FromDishka[UnitOfWork],
            task_permissions_repository: FromDishka[TaskPermissionsRepository],
            tasks_repository: FromDishka[TasksRepository],
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor]
    ) -> DeleteTaskPermission:
        return DeleteTaskPermission(
            uow=uow,
            task_permissions_repository=task_permissions_repository,
            tasks_repository=tasks_repository,
            users_repository=users_repository,
            jwt_processor=jwt_processor,
        )
