from app.application.protocols.interactor import Interactor

# dto
from app.application.dto.tasks import (
    CreateTaskRequest,
    TaskResponse
)

# entities
from app.domain.entities.tasks import TaskEntity

# value objects
from app.domain.value_objects.id import IdVO

# repositories [domain]
from app.domain.protocols.repositories.uow import UnitOfWork
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.protocols.repositories.users import UsersRepository

# adapters [domain]
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# exceptions
from app.domain.exceptions.users import UserNotFoundException


class CreateTask(Interactor[CreateTaskRequest, TaskResponse]):

    def __init__(
            self,
            uow: UnitOfWork,
            tasks_repository: TasksRepository,
            users_repository: UsersRepository,
            id_provider: IdProvider,
            jwt_processor: JwtTokenProcessor,
    ) -> None:
        self.uow = uow
        self.tasks_repository = tasks_repository
        self.users_repository = users_repository
        self.id_provider = id_provider
        self.jwt_processor = jwt_processor

    async def __call__(self, request: CreateTaskRequest) -> TaskResponse:
        user_id = self.jwt_processor.get_current_user_id()

        user_entity = await self.users_repository.get_by_id(id=user_id)

        if not user_entity:
            raise UserNotFoundException("User not found, something went wrong")

        task_entity = TaskEntity(
            id=IdVO(self.id_provider.generate_uuid()),
            name=request.name,
            description=request.description,
            user_id=user_entity.id
        )

        await self.tasks_repository.create(entity=task_entity)
        await self.uow.commit()

        return TaskResponse.from_entity(task_entity)
