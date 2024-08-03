from uuid import UUID
from app.application.protocols.interactor import Interactor

# dto

# entities

# value objects
from app.domain.value_objects.id import IdVO

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# exceptions
from app.domain.exceptions.users import UserNotFoundException
from app.domain.exceptions.task_permissions import PermissionDeniedException


class DeleteTask(Interactor[UUID, None]):

    def __init__(
            self,
            uow: UnitOfWork,
            tasks_repository: TasksRepository,
            users_repository: UsersRepository,
            jwt_processor: JwtTokenProcessor
    ) -> None:
        self.uow = uow
        self.tasks_repository = tasks_repository
        self.users_repository = users_repository
        self.jwt_processor = jwt_processor

    async def __call__(self, request: UUID) -> None:
        user_id = self.jwt_processor.get_current_user_id()
        current_user_entity = await self.users_repository.get_by_id(id=user_id)

        if not current_user_entity:
            raise UserNotFoundException("User not found, something went wrong")

        is_owner = await self.tasks_repository.is_owner(id=IdVO(request), user_id=current_user_entity.id)

        if not is_owner:
            raise PermissionDeniedException("You do not have permission to perform this action")

        await self.tasks_repository.delete(id=IdVO(request))
        await self.uow.commit()

        return
