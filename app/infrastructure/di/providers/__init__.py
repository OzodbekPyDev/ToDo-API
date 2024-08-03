from dishka import make_async_container
from app.infrastructure.di.providers.db import DBProvider
from app.infrastructure.di.providers.adapters import AdaptersProvider
from app.infrastructure.di.providers.repositories import RepositoriesProvider

from app.infrastructure.di.providers.interactors.users import UsersInteractorProvider
from app.infrastructure.di.providers.interactors.tasks import TasksInteractorProvider
from app.infrastructure.di.providers.interactors.task_permissions import TaskPermissionsInteractorProvider

container = make_async_container(
    DBProvider(),
    RepositoriesProvider(),
    AdaptersProvider(),
    UsersInteractorProvider(),
    TasksInteractorProvider(),
    TaskPermissionsInteractorProvider(),
)
