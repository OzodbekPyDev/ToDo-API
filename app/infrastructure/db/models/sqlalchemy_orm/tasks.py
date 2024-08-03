from uuid import UUID
from app.infrastructure.db.models.sqlalchemy_orm.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# entities
from app.domain.entities.tasks import TaskEntity

# value objects
from app.domain.value_objects.id import IdVO


class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))

    def to_entity(self) -> TaskEntity:
        return TaskEntity(
            id=IdVO(self.id),
            name=self.name,
            description=self.description,
            user_id=IdVO(self.user_id)
        )
