from uuid import UUID
from app.application.protocols.interactor import Interactor

# dto
from app.application.dto.tasks import (
    FilterTasksRequest,
    TaskResponse
)

# entities
from app.domain.entities.task_permissions import PermissionType

# value objects
from app.domain.value_objects.id import IdVO

# repositories [domain]
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# exceptions
from app.domain.exceptions.tasks import TaskNotFoundException
from app.domain.exceptions.users import UserNotFoundException
from app.domain.exceptions.task_permissions import PermissionDeniedException

# filter params
from app.domain.entities.filter_params.tasks import TasksFilterParams


class GetAllTasks(Interactor[FilterTasksRequest, list[TaskResponse]]):
    """By default user gets only own tasks"""

    def __init__(
            self,
            tasks_repository: TasksRepository,
            users_repository: UsersRepository,
            jwt_processor: JwtTokenProcessor
    ) -> None:
        self.tasks_repository = tasks_repository
        self.users_repository = users_repository
        self.jwt_processor = jwt_processor

    async def __call__(self, request: FilterTasksRequest) -> list[TaskResponse]:

        user_id = self.jwt_processor.get_current_user_id()
        user_entity = await self.users_repository.get_by_id(id=user_id)
        if not user_entity:
            raise UserNotFoundException("User not found, something went wrong!")

        filter_params = TasksFilterParams(
            user_id=user_entity.id,
            name=request.name
        )

        task_entities = await self.tasks_repository.get_all(
            filter_params=filter_params
        )

        return [TaskResponse.from_entity(entity=task_entity) for task_entity in task_entities]


class GetTaskById(Interactor[UUID, TaskResponse]):

    def __init__(
            self,
            tasks_repository: TasksRepository,
            task_permissions_repository: TaskPermissionsRepository,
            users_repository: UsersRepository,
            jwt_processor: JwtTokenProcessor
    ) -> None:
        self.tasks_repository = tasks_repository
        self.task_permissions_repository = task_permissions_repository
        self.users_repository = users_repository
        self.jwt_processor = jwt_processor

    async def __call__(self, request: UUID) -> TaskResponse:
        user_id = self.jwt_processor.get_current_user_id()
        user_entity = await self.users_repository.get_by_id(id=user_id)
        if not user_entity:
            raise UserNotFoundException("User not found, something went wrong!")

        task_entity = await self.tasks_repository.get_by_id(id=IdVO(request))

        if not task_entity:
            raise TaskNotFoundException("Task not found, something went wrong!")

        # if the current_user is owner
        if task_entity.user_id != user_entity.id:
            # if the current user has permission to view the task
            has_permission = await self.task_permissions_repository.has_permission(
                task_id=task_entity.id,
                user_id=user_entity.id,
                permissions=[PermissionType.VIEWER, PermissionType.EDITOR]
            )
            if not has_permission:
                raise PermissionDeniedException("You do not have permission to perform this action")

        return TaskResponse.from_entity(entity=task_entity)
