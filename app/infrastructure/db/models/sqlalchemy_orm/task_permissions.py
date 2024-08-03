from uuid import UUID
from app.infrastructure.db.models.sqlalchemy_orm.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# entities
from app.domain.entities.task_permissions import TaskPermissionEntity, PermissionType

# value objects
from app.domain.value_objects.id import IdVO


class TaskPermission(Base):
    __tablename__ = "task_permissions"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete='CASCADE'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    permission: Mapped[PermissionType]

    def to_entity(self) -> TaskPermissionEntity:
        return TaskPermissionEntity(
            id=IdVO(self.id),
            task_id=IdVO(self.task_id),
            user_id=IdVO(self.user_id),
            permission=self.permission
        )
