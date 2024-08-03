from dataclasses import dataclass
from uuid import UUID

# entities
from app.domain.entities.tasks import TaskEntity


@dataclass
class CreateTaskRequest:
    name: str
    description: str


@dataclass
class UpdateTaskRequest:
    id: UUID
    name: str
    description: str


@dataclass
class TaskResponse:
    id: UUID
    name: str
    description: str
    user_id: UUID

    @classmethod
    def from_entity(cls, entity: TaskEntity) -> "TaskResponse":
        return cls(
            id=entity.id.value,
            name=entity.name,
            description=entity.description,
            user_id=entity.user_id.value
        )


@dataclass
class FilterTasksRequest:
    name: str | None = None
