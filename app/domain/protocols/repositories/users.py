from typing import Protocol

# entities
from app.domain.entities.users import UserEntity

# value objects
from app.domain.value_objects.id import IdVO


class UsersRepository(Protocol):

    async def create(self, entity: UserEntity) -> None:
        raise NotImplementedError

    async def get_all(self) -> list[UserEntity]:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> UserEntity | None:
        raise NotImplementedError

    async def get_by_id(self, id: IdVO) -> UserEntity | None:
        raise NotImplementedError
