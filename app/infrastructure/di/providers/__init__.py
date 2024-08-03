from dishka import make_async_container, AsyncContainer
from app.infrastructure.di.providers.db import DBProvider
from app.infrastructure.di.providers.adapters import AdaptersProvider
from app.infrastructure.di.providers.repositories import RepositoriesProvider

from app.infrastructure.di.providers.interactors.users import UsersInteractorProvider
from app.infrastructure.di.providers.interactors.tasks import TasksInteractorProvider
from app.infrastructure.di.providers.interactors.task_permissions import TaskPermissionsInteractorProvider


def create_async_container(db_url: str) -> AsyncContainer:

    prod_container = make_async_container(
        DBProvider(db_url=db_url),
        RepositoriesProvider(),
        AdaptersProvider(),
        UsersInteractorProvider(),
        TasksInteractorProvider(),
        TaskPermissionsInteractorProvider(),
    )
    return prod_container


