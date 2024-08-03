from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete

# protocols [domain]
from app.domain.protocols.repositories.tasks import TasksRepository
from app.domain.value_objects.id import IdVO

# models
from app.infrastructure.db.models.sqlalchemy_orm.tasks import Task

# entities
from app.domain.entities.tasks import TaskEntity

# filter params
from app.domain.entities.filter_params.tasks import TasksFilterParams

# exceptions
from app.domain.exceptions.tasks import TaskNotFoundException


class SqlalchemyTasksRepository(TasksRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, entity: TaskEntity) -> None:
        stmt = (
            insert(Task)
            .values(
                id=entity.id.value,
                name=entity.name,
                description=entity.description,
                user_id=entity.user_id.value
            )
        )
        await self.session.execute(stmt)

    async def get_all(self, filter_params: TasksFilterParams) -> list[TaskEntity]:
        stmt = select(Task).where(Task.user_id == filter_params.user_id.value)

        if filter_params.name:
            stmt = stmt.where(Task.name.ilike(f"%{filter_params.name}%"))

        result = await self.session.execute(stmt)
        tasks = result.scalars().all()
        return [task.to_entity() for task in tasks]

    async def get_by_id(self, id: IdVO) -> TaskEntity | None:
        stmt = select(Task).where(Task.id == id.value)
        result = await self.session.execute(stmt)
        task = result.scalar_one_or_none()
        return task.to_entity() if task else None

    async def update(self, entity: TaskEntity) -> None:
        stmt = (
            update(Task)
            .where(Task.id == entity.id.value)
            .values(
                name=entity.name,
                description=entity.description
            )
        )

        await self.session.execute(stmt)

    async def delete(self, id: IdVO) -> None:
        stmt = delete(Task).where(Task.id == id.value)
        await self.session.execute(stmt)

    async def is_owner(self, id: IdVO, user_id: IdVO) -> bool:
        task_entity = await self.get_by_id(id=id)
        if not task_entity:
            raise TaskNotFoundException("Task not found")
        return task_entity.user_id == user_id
