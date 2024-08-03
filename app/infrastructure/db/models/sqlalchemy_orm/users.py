from app.infrastructure.db.models.sqlalchemy_orm.base import Base
from sqlalchemy.orm import Mapped, mapped_column

# entities
from app.domain.entities.users import UserEntity

# value objects
from app.domain.value_objects.id import IdVO


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=IdVO(value=self.id),
            email=self.email,
            password=self.password
        )
