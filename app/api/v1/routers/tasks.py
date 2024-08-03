from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

# dto
from app.application.dto.tasks import (
    CreateTaskRequest,
    UpdateTaskRequest,
    TaskResponse,
    FilterTasksRequest
)

# schemes
from app.api.v1.schemes.tasks import UpdateTaskSchema

# use cases
from app.application.use_cases.tasks.create import CreateTask
from app.application.use_cases.tasks.get import GetAllTasks, GetTaskById
from app.application.use_cases.tasks.update import UpdateTask
from app.application.use_cases.tasks.delete import DeleteTask

# dependencies
from app.api.v1.routers.dependencies.auth import auth_required


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    route_class=DishkaRoute,
    dependencies=[Depends(auth_required)]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
        request: CreateTaskRequest,
        create_task_interactor: FromDishka[CreateTask]
) -> TaskResponse:
    return await create_task_interactor(request)


@router.get("/")
async def get_all_tasks_of_current_user(
        request: Annotated[FilterTasksRequest, Depends()],
        get_all_tasks_interactor: FromDishka[GetAllTasks]
) -> list[TaskResponse]:
    return await get_all_tasks_interactor(request)


@router.get("/{id}")
async def get_task_by_id(
        id: UUID,
        get_task_by_id_interactor: FromDishka[GetTaskById]
) -> TaskResponse:
    return await get_task_by_id_interactor(id)


@router.put("/{id}")
async def update_task(
        id: UUID,
        data: UpdateTaskSchema,
        update_task_interactor: FromDishka[UpdateTask]
) -> TaskResponse:
    request = UpdateTaskRequest(
        id=id,
        name=data.name,
        description=data.description
    )

    return await update_task_interactor(request)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        id: UUID,
        delete_task_interactor: FromDishka[DeleteTask]
) -> None:
    return await delete_task_interactor(id)
