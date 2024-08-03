from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka

# use cases
from app.application.use_cases.tasks.create import CreateTask
from app.application.use_cases.tasks.get import GetAllTasks, GetTaskById
from app.application.use_cases.tasks.update import UpdateTask
from app.application.use_cases.tasks.delete import DeleteTask

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor


class TasksInteractorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_create(
            self,
            uow: FromDishka[UnitOfWork],
            tasks_repository: FromDishka[TasksRepository],
            users_repository: FromDishka[UsersRepository],
            id_provider: FromDishka[IdProvider],
            jwt_processor: FromDishka[JwtTokenProcessor]
    ) -> CreateTask:
        return CreateTask(
            uow=uow,
            tasks_repository=tasks_repository,
            users_repository=users_repository,
            id_provider=id_provider,
            jwt_processor=jwt_processor
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_all(
            self,
            tasks_repository: FromDishka[TasksRepository],
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor]
    ) -> GetAllTasks:
        return GetAllTasks(
            tasks_repository=tasks_repository,
            users_repository=users_repository,
            jwt_processor=jwt_processor
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_by_id(
            self,
            tasks_repository: FromDishka[TasksRepository],
            task_permissions_repository: FromDishka[TaskPermissionsRepository],
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor],
    ) -> GetTaskById:
        return GetTaskById(
            tasks_repository=tasks_repository,
            task_permissions_repository=task_permissions_repository,
            users_repository=users_repository,
            jwt_processor=jwt_processor
        )

    @provide(scope=Scope.REQUEST)
    def provide_update(
            self,
            uow: FromDishka[UnitOfWork],
            tasks_repository: FromDishka[TasksRepository],
            task_permissions_repository: FromDishka[TaskPermissionsRepository],
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor],
    ) -> UpdateTask:
        return UpdateTask(
            uow=uow,
            tasks_repository=tasks_repository,
            task_permissions_repository=task_permissions_repository,
            users_repository=users_repository,
            jwt_processor=jwt_processor
        )

    @provide(scope=Scope.REQUEST)
    def provide_delete(
            self,
            uow: FromDishka[UnitOfWork],
            tasks_repository: FromDishka[TasksRepository],
            users_repository: FromDishka[UsersRepository],
            jwt_processor: FromDishka[JwtTokenProcessor],
    ) -> DeleteTask:
        return DeleteTask(
            uow=uow,
            tasks_repository=tasks_repository,
            users_repository=users_repository,
            jwt_processor=jwt_processor
        )
