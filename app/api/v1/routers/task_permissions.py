from uuid import UUID
from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

# dto
from app.application.dto.task_permissions import (
    CreateTaskPermissionRequest,
    UpdateTaskPermissionRequest,
    TaskPermissionResponse
)

# schemes
from app.api.v1.schemes.task_permissions import UpdateTaskPermissionSchema

# use cases
from app.application.use_cases.task_permissions.create import CreateTaskPermission
from app.application.use_cases.task_permissions.get import (
    GetAllTaskPermissionsGrantedToUser,
    GetAllTaskPermissionsGrantedToTask
)
from app.application.use_cases.task_permissions.update import UpdateTaskPermission
from app.application.use_cases.task_permissions.delete import DeleteTaskPermission

# dependencies
from app.api.v1.routers.dependencies.auth import auth_required


router = APIRouter(
    prefix="/task-permissions",
    tags=["Task Permissions"],
    route_class=DishkaRoute,
    dependencies=[Depends(auth_required)]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_task_permission(
        request: CreateTaskPermissionRequest,
        create_task_permission_interactor: FromDishka[CreateTaskPermission]
) -> TaskPermissionResponse:
    return await create_task_permission_interactor(request)


@router.get('/')
async def get_task_permissions_granted_to_current_user(
        get_task_permissions_granted_to_user_interactor: FromDishka[GetAllTaskPermissionsGrantedToUser]
) -> list[TaskPermissionResponse]:
    return await get_task_permissions_granted_to_user_interactor()


@router.get('/{task_id}')
async def get_task_permissions_granted_to_task(
        task_id: UUID,
        get_task_permissions_granted_to_task_interactor: FromDishka[GetAllTaskPermissionsGrantedToTask]
) -> list[TaskPermissionResponse]:
    return await get_task_permissions_granted_to_task_interactor(task_id)


@router.put('/{id}')
async def update_task_permission(
        id: UUID,
        data: UpdateTaskPermissionSchema,
        update_task_permission_interactor: FromDishka[UpdateTaskPermission]
) -> TaskPermissionResponse:
    request = UpdateTaskPermissionRequest(
        id=id,
        permission=data.permission
    )

    return await update_task_permission_interactor(request)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_permission(
        id: UUID,
        delete_task_permission_interactor: FromDishka[DeleteTaskPermission]
) -> None:
    return await delete_task_permission_interactor(id)
