from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

# protocols [domain]
from app.domain.protocols.repositories.users import UsersRepository
from app.domain.value_objects.id import IdVO

# models
from app.infrastructure.db.models.sqlalchemy_orm.users import User

# entities
from app.domain.entities.users import UserEntity


class SqlalchemyUsersRepository(UsersRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, entity: UserEntity) -> None:
        stmt = (
            insert(User)
            .values(
                id=entity.id.value,
                email=entity.email,
                password=entity.password
            )
        )
        await self.session.execute(stmt)

    async def get_all(self) -> list[UserEntity]:
        stmt = select(User)
        result = await self.session.execute(stmt)
        user_entities = result.scalars().all()
        return [user_entity.to_entity() for user_entity in user_entities]

    async def get_by_email(self, email: str) -> UserEntity | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        return item.to_entity() if item else None

    async def get_by_id(self, id: IdVO) -> UserEntity | None:
        stmt = select(User).where(User.id == id.value)
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        return item.to_entity() if item else None
