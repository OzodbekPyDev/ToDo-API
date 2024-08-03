from dataclasses import dataclass

# value objects
from app.domain.value_objects.id import IdVO


@dataclass
class TasksFilterParams:
    user_id: IdVO
    name: str | None
