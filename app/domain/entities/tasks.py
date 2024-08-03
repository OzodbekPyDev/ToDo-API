from dataclasses import dataclass

from app.domain.entities.base import BaseEntity

from app.domain.value_objects.id import IdVO


@dataclass
class TaskEntity(BaseEntity):
    name: str
    description: str
    user_id: IdVO

    def __init__(
            self,
            id: IdVO,
            name: str,
            description: str,
            user_id: IdVO
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.user_id = user_id

    def update(
            self,
            name: str,
            description: str
    ) -> None:
        self.name = name
        self.description = description
