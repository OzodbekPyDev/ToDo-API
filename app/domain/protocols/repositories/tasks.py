from typing import Protocol

# entities
from app.domain.entities.tasks import TaskEntity

# value objects
from app.domain.value_objects.id import IdVO

# filter params
from app.domain.entities.filter_params.tasks import TasksFilterParams


class TasksRepository(Protocol):

    async def create(self, entity: TaskEntity) -> None:
        raise NotImplementedError

    async def get_all(self, filter_params: TasksFilterParams) -> list[TaskEntity]:
        raise NotImplementedError

    async def get_by_id(self, id: IdVO) -> TaskEntity | None:
        raise NotImplementedError

    async def update(self, entity: TaskEntity) -> None:
        raise NotImplementedError

    async def delete(self, id: IdVO) -> None:
        raise NotImplementedError

    async def is_owner(self, id: IdVO, user_id: IdVO) -> bool:
        raise NotImplementedError
