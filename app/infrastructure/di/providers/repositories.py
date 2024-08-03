from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

# repositories[domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.users import UsersRepository
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository

# repositories [infrastructure/sqlalchemy orm]
from app.infrastructure.repositories.sqlalchemy_orm.uow import \
    SqlalchemyUnitOfWork
from app.infrastructure.repositories.sqlalchemy_orm.users import \
    SqlalchemyUsersRepository
from app.infrastructure.repositories.sqlalchemy_orm.tasks import \
    SqlalchemyTasksRepository
from app.infrastructure.repositories.sqlalchemy_orm.task_permissions import \
    SqlalchemyTaskPermissionsRepository


class RepositoriesProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_uow_repository(self, session: FromDishka[AsyncSession]) -> UnitOfWork:
        return SqlalchemyUnitOfWork(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_users_repository(self, session: FromDishka[AsyncSession]) -> UsersRepository:
        return SqlalchemyUsersRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_tasks_repository(self, session: FromDishka[AsyncSession]) -> TasksRepository:
        return SqlalchemyTasksRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def provide_task_permissions_repository(self, session: FromDishka[AsyncSession]) -> TaskPermissionsRepository:
        return SqlalchemyTaskPermissionsRepository(session=session)
