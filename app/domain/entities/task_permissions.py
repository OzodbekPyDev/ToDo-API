from dataclasses import dataclass
from enum import Enum

from app.domain.entities.base import BaseEntity

from app.domain.value_objects.id import IdVO


class PermissionType(Enum):
    VIEWER = "viewer"
    EDITOR = "editor"


@dataclass
class TaskPermissionEntity(BaseEntity):
    task_id: IdVO
    user_id: IdVO
    permission: PermissionType

    def __init__(
            self,
            id: IdVO,
            task_id: IdVO,
            user_id: IdVO,
            permission: PermissionType,
    ) -> None:
        self.id = id
        self.task_id = task_id
        self.user_id = user_id
        self.permission = permission

    def update(
            self,
            permission: PermissionType
    ) -> None:
        self.permission = permission
