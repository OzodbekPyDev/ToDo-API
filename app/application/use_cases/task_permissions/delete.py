from uuid import UUID
from app.application.protocols.interactor import Interactor

# dto

# entities

# value objects
from app.domain.value_objects.id import IdVO

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# exceptions
from app.domain.exceptions.users import UserNotFoundException
from app.domain.exceptions.task_permissions import PermissionDeniedException, TaskPermissionNotFoundException


class DeleteTaskPermission(Interactor[UUID, None]):

    def __init__(
            self,
            uow: UnitOfWork,
            task_permissions_repository: TaskPermissionsRepository,
            tasks_repository: TasksRepository,
            users_repository: UsersRepository,
            jwt_processor: JwtTokenProcessor,
    ) -> None:
        self.uow = uow
        self.task_permissions_repository = task_permissions_repository
        self.tasks_repository = tasks_repository
        self.users_repository = users_repository
        self.jwt_processor = jwt_processor

    async def __call__(self, request: UUID) -> None:
        user_id = self.jwt_processor.get_current_user_id()
        user_entity = await self.users_repository.get_by_id(id=user_id)
        if not user_entity:
            raise UserNotFoundException("User not found, something went wrong")

        task_permission_entity = await self.task_permissions_repository.get_by_id(id=IdVO(request))
        if not task_permission_entity:
            raise TaskPermissionNotFoundException("Task permission not found")

        is_owner = await self.tasks_repository.is_owner(id=task_permission_entity.task_id, user_id=user_entity.id)
        if not is_owner:
            raise PermissionDeniedException("You do not have permission to delete this task permission because you are not the owner of the task")

        await self.task_permissions_repository.delete(id=task_permission_entity.id)
        await self.uow.commit()

        return
