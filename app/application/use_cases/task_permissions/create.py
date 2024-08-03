from app.application.protocols.interactor import Interactor

# dto
from app.application.dto.task_permissions import (
    CreateTaskPermissionRequest,
    TaskPermissionResponse
)

# entities
from app.domain.entities.task_permissions import TaskPermissionEntity

# value objects
from app.domain.value_objects.id import IdVO

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# exceptions
from app.domain.exceptions.users import UserNotFoundException
from app.domain.exceptions.task_permissions import PermissionDeniedException


class CreateTaskPermission(Interactor[CreateTaskPermissionRequest, TaskPermissionResponse]):

    def __init__(
            self,
            uow: UnitOfWork,
            task_permissions_repository: TaskPermissionsRepository,
            tasks_repository: TasksRepository,
            users_repository: UsersRepository,
            id_provider: IdProvider,
            jwt_processor: JwtTokenProcessor,
    ) -> None:
        self.uow = uow
        self.task_permissions_repository = task_permissions_repository
        self.tasks_repository = tasks_repository
        self.users_repository = users_repository
        self.id_provider = id_provider
        self.jwt_processor = jwt_processor

    async def __call__(self, request: CreateTaskPermissionRequest) -> TaskPermissionResponse:
        user_id = self.jwt_processor.get_current_user_id()
        user_entity = await self.users_repository.get_by_id(id=user_id)
        if not user_entity:
            raise UserNotFoundException("User not found, something went wrong")

        is_owner = await self.tasks_repository.is_owner(id=IdVO(request.task_id), user_id=user_entity.id)
        if not is_owner:
            raise PermissionDeniedException("You do not have permission to modify access to this task because you are not the owner")

        task_permission_entity = TaskPermissionEntity(
            id=IdVO(self.id_provider.generate_uuid()),
            task_id=IdVO(request.task_id),
            user_id=IdVO(request.user_id),
            permission=request.permission
        )

        await self.task_permissions_repository.create(entity=task_permission_entity)
        await self.uow.commit()

        return TaskPermissionResponse.from_entity(task_permission_entity)
