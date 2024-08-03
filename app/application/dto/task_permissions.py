from dataclasses import dataclass
from uuid import UUID

# entities
from app.domain.entities.task_permissions import TaskPermissionEntity, PermissionType


@dataclass
class CreateTaskPermissionRequest:
    task_id: UUID
    user_id: UUID
    permission: PermissionType


@dataclass
class UpdateTaskPermissionRequest:
    id: UUID
    permission: PermissionType


@dataclass
class TaskPermissionResponse:
    id: UUID
    task_id: UUID
    user_id: UUID
    permission: PermissionType

    @classmethod
    def from_entity(cls, entity: TaskPermissionEntity) -> "TaskPermissionResponse":
        return cls(
            id=entity.id.value,
            task_id=entity.task_id.value,
            user_id=entity.user_id.value,
            permission=entity.permission
        )
