from app.application.protocols.interactor import Interactor

# dto
from app.application.dto.tasks import (
    UpdateTaskRequest,
    TaskResponse
)

# entities
from app.domain.entities.task_permissions import PermissionType

# value objects
from app.domain.value_objects.id import IdVO

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# exceptions
from app.domain.exceptions.tasks import TaskNotFoundException
from app.domain.exceptions.users import UserNotFoundException
from app.domain.exceptions.task_permissions import PermissionDeniedException


class UpdateTask(Interactor[UpdateTaskRequest, TaskResponse]):

    def __init__(
            self,
            uow: UnitOfWork,
            tasks_repository: TasksRepository,
            task_permissions_repository: TaskPermissionsRepository,
            users_repository: UsersRepository,
            jwt_processor: JwtTokenProcessor
    ) -> None:
        self.uow = uow
        self.tasks_repository = tasks_repository
        self.task_permissions_repository = task_permissions_repository
        self.users_repository = users_repository
        self.jwt_processor = jwt_processor

    async def __call__(self, request: UpdateTaskRequest) -> TaskResponse:
        user_id = self.jwt_processor.get_current_user_id()
        current_user_entity = await self.users_repository.get_by_id(id=user_id)
        if not current_user_entity:
            raise UserNotFoundException("User not found, something went wrong")

        task_entity = await self.tasks_repository.get_by_id(id=IdVO(request.id))

        if not task_entity:
            raise TaskNotFoundException("Task not found!")

        if task_entity.user_id != current_user_entity.id:
            has_permission = await self.task_permissions_repository.has_permission(
                task_id=task_entity.id,
                user_id=current_user_entity.id,
                permissions=[PermissionType.EDITOR]
            )
            if not has_permission:
                raise PermissionDeniedException("You do not have permission to perform this action")

        task_entity.update(
            name=request.name,
            description=request.description
        )

        await self.tasks_repository.update(entity=task_entity)
        await self.uow.commit()

        return TaskResponse.from_entity(task_entity)
