from dataclasses import dataclass

from app.domain.entities.task_permissions import PermissionType


@dataclass
class UpdateTaskPermissionSchema:
    permission: PermissionType
