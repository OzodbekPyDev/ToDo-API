from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete

# protocols [domain]
from app.domain.protocols.repositories.task_permissions import TaskPermissionsRepository
from app.domain.value_objects.id import IdVO

# models
from app.infrastructure.db.models.sqlalchemy_orm.task_permissions import TaskPermission

# entities
from app.domain.entities.task_permissions import TaskPermissionEntity, PermissionType


class SqlalchemyTaskPermissionsRepository(TaskPermissionsRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, entity: TaskPermissionEntity) -> None:
        stmt = (
            insert(TaskPermission)
            .values(
                id=entity.id.value,
                task_id=entity.task_id.value,
                user_id=entity.user_id.value,
                permission=entity.permission
            )
        )

        await self.session.execute(stmt)

    async def get_all_granted_to_user(self, user_id: IdVO) -> list[TaskPermissionEntity]:
        stmt = select(TaskPermission).where(TaskPermission.user_id == user_id.value)
        result = await self.session.execute(stmt)
        task_permissions = result.scalars().all()
        return [task_permission.to_entity() for task_permission in task_permissions]

    async def get_all_granted_to_task(self, task_id: IdVO) -> list[TaskPermissionEntity]:
        stmt = select(TaskPermission).where(TaskPermission.task_id == task_id.value)
        result = await self.session.execute(stmt)
        task_permissions = result.scalars().all()
        return [task_permission.to_entity() for task_permission in task_permissions]

    async def get_by_id(self, id: IdVO) -> TaskPermissionEntity | None:
        stmt = select(TaskPermission).where(TaskPermission.id == id.value)
        result = await self.session.execute(stmt)
        task_permission = result.scalar_one_or_none()
        return task_permission.to_entity() if task_permission else None

    async def update(self, entity: TaskPermissionEntity) -> None:
        stmt = (
            update(TaskPermission)
            .where(TaskPermission.id == entity.id.value)
            .values(
                permission=entity.permission
            )
        )

        await self.session.execute(stmt)

    async def delete(self, id: IdVO) -> None:
        stmt = delete(TaskPermission).where(TaskPermission.id == id.value)

        await self.session.execute(stmt)

    async def has_permission(
            self,
            task_id: IdVO,
            user_id: IdVO,
            permissions: list[PermissionType]
    ) -> bool:
        stmt = (
            select(TaskPermission)
            .where(
                TaskPermission.task_id == task_id.value,
                TaskPermission.user_id == user_id.value,
                TaskPermission.permission.in_(permissions)
            )
        )

        result = await self.session.execute(stmt)
        task_permission = result.scalar_one_or_none()

        return task_permission is not None
