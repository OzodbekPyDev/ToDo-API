import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_create_task(authorized_client: AsyncClient):

    response = await authorized_client.post("/api/v1/tasks/", json={
        "name": "Test Task",
        "description": "This is a test task description"
    })

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Task"
    assert data["description"] == "This is a test task description"


@pytest.mark.asyncio
async def test_get_all_tasks(authorized_client: AsyncClient):

    response = await authorized_client.get("/api/v1/tasks/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(task["name"] == "Test Task" for task in data)


@pytest.mark.asyncio
async def test_get_task_by_id(authorized_client: AsyncClient):
    # Firstly create a task in order to get its ID
    create_response = await authorized_client.post("/api/v1/tasks/", json={
        "name": "Test Task",
        "description": "This is a test task description"
    })

    assert create_response.status_code == status.HTTP_201_CREATED
    task = create_response.json()
    task_id = task["id"]

    # Get a task by ID
    response = await authorized_client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["name"] == "Test Task"
    assert data["description"] == "This is a test task description"


@pytest.mark.asyncio
async def test_update_task(authorized_client: AsyncClient):
    # Create a test task first in order to get its ID to update
    create_response = await authorized_client.post("/api/v1/tasks/", json={
        "name": "Test Task",
        "description": "This is a test task description"
    })

    assert create_response.status_code == status.HTTP_201_CREATED
    task = create_response.json()
    task_id = task["id"]

    # Update a task by ID
    response = await authorized_client.put(f"/api/v1/tasks/{task_id}", json={
        "name": "Updated Task",
        "description": "This is an updated task description"
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["name"] == "Updated Task"
    assert data["description"] == "This is an updated task description"


@pytest.mark.asyncio
async def test_delete_task(authorized_client: AsyncClient):
    # Firstly create a task in order to get its ID to delete
    create_response = await authorized_client.post("/api/v1/tasks/", json={
        "name": "Test Task",
        "description": "This is a test task description"
    })
    assert create_response.status_code == status.HTTP_201_CREATED
    task = create_response.json()
    task_id = task["id"]

    # Delete a task by ID
    response = await authorized_client.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the task was indeed deleted
    response = await authorized_client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
