from uuid import UUID
from app.application.protocols.interactor import Interactor

# dto
from app.application.dto.task_permissions import (
    TaskPermissionResponse
)

# entities

# value objects
from app.domain.value_objects.id import IdVO

# repositories [domain]
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# exceptions
from app.domain.exceptions.users import UserNotFoundException
from app.domain.exceptions.task_permissions import PermissionDeniedException


class GetAllTaskPermissionsGrantedToUser(Interactor[None, list[TaskPermissionResponse]]):

    def __init__(
            self,
            task_permissions_repository: TaskPermissionsRepository,
            users_repository: UsersRepository,
            jwt_processor: JwtTokenProcessor,
    ) -> None:
        self.task_permissions_repository = task_permissions_repository
        self.users_repository = users_repository
        self.jwt_processor = jwt_processor

    async def __call__(self, request: None = None) -> list[TaskPermissionResponse]:
        user_id = self.jwt_processor.get_current_user_id()
        user_entity = await self.users_repository.get_by_id(id=user_id)
        if not user_entity:
            raise UserNotFoundException("User not found, something went wrong")

        task_permission_entities = await self.task_permissions_repository.get_all_granted_to_user(
            user_id=user_entity.id
        )

        return [TaskPermissionResponse.from_entity(task_permission_entity)
                for task_permission_entity in task_permission_entities]


class GetAllTaskPermissionsGrantedToTask(Interactor[UUID, list[TaskPermissionResponse]]):

    def __init__(
            self,
            task_permissions_repository: TaskPermissionsRepository,
            users_repository: UsersRepository,
            tasks_repository: TasksRepository,
            jwt_processor: JwtTokenProcessor,
    ) -> None:
        self.task_permissions_repository = task_permissions_repository
        self.users_repository = users_repository
        self.tasks_repository = tasks_repository
        self.jwt_processor = jwt_processor

    async def __call__(self, request: UUID) -> list[TaskPermissionResponse]:
        user_id = self.jwt_processor.get_current_user_id()
        user_entity = await self.users_repository.get_by_id(id=user_id)
        if not user_entity:
            raise UserNotFoundException("User not found, something went wrong")

        is_owner = await self.tasks_repository.is_owner(
            id=IdVO(request), user_id=user_entity.id
        )
        if not is_owner:
            raise PermissionDeniedException("You do not have permission to view permissions for this task.")

        task_permission_entities = await self.task_permissions_repository.get_all_granted_to_task(
            task_id=IdVO(request)
        )

        return [TaskPermissionResponse.from_entity(task_permission_entity)
                for task_permission_entity in task_permission_entities]
