from typing import Protocol

# entities
from app.domain.entities.task_permissions import TaskPermissionEntity, PermissionType

# value objects
from app.domain.value_objects.id import IdVO


class TaskPermissionsRepository(Protocol):

    async def create(self, entity: TaskPermissionEntity) -> None:
        raise NotImplementedError

    async def get_all_granted_to_user(self, user_id: IdVO) -> list[TaskPermissionEntity]:
        raise NotImplementedError

    async def get_all_granted_to_task(self, task_id: IdVO) -> list[TaskPermissionEntity]:
        raise NotImplementedError

    async def get_by_id(self, id: IdVO) -> TaskPermissionEntity | None:
        raise NotImplementedError

    async def update(self, entity: TaskPermissionEntity) -> None:
        raise NotImplementedError

    async def delete(self, id: IdVO) -> None:
        raise NotImplementedError

    async def has_permission(
            self,
            task_id: IdVO,
            user_id: IdVO,
            permissions: list[PermissionType]
    ) -> bool:
        raise NotImplementedError
