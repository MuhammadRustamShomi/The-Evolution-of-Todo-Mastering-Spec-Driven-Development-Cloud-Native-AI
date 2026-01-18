"""Task endpoint tests."""

import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, auth_headers):
    """Test creating a task."""
    response = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["priority"] == "high"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_create_task_minimal(client: AsyncClient, auth_headers):
    """Test creating a task with minimal data."""
    response = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Minimal Task"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["priority"] == "medium"  # Default


@pytest.mark.asyncio
async def test_create_task_unauthorized(client: AsyncClient):
    """Test creating task without auth fails."""
    response = await client.post(
        "/api/tasks",
        json={"title": "Unauthorized Task"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient, auth_headers):
    """Test listing tasks."""
    # Create some tasks
    for i in range(3):
        await client.post(
            "/api/tasks",
            headers=auth_headers,
            json={"title": f"Task {i}"},
        )

    response = await client.get("/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_list_tasks_with_status_filter(client: AsyncClient, auth_headers):
    """Test filtering tasks by status."""
    # Create pending and done tasks
    await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Pending Task"},
    )
    create_resp = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Done Task"},
    )
    task_id = create_resp.json()["id"]

    # Mark one as done
    await client.post(f"/api/tasks/{task_id}/done", headers=auth_headers)

    # Filter by pending
    response = await client.get("/api/tasks?status=pending", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Pending Task"


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient, auth_headers):
    """Test getting a specific task."""
    create_resp = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Get Me Task"},
    )
    task_id = create_resp.json()["id"]

    response = await client.get(f"/api/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Me Task"


@pytest.mark.asyncio
async def test_get_task_not_found(client: AsyncClient, auth_headers):
    """Test getting nonexistent task returns 404."""
    fake_id = uuid4()
    response = await client.get(f"/api/tasks/{fake_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, auth_headers):
    """Test updating a task."""
    create_resp = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Original Title"},
    )
    task_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/tasks/{task_id}",
        headers=auth_headers,
        json={"title": "Updated Title", "priority": "high"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["priority"] == "high"


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, auth_headers):
    """Test deleting a task."""
    create_resp = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Delete Me"},
    )
    task_id = create_resp.json()["id"]

    response = await client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify deleted
    get_resp = await client.get(f"/api/tasks/{task_id}", headers=auth_headers)
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_mark_task_done(client: AsyncClient, auth_headers):
    """Test marking a task as done."""
    create_resp = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Complete Me"},
    )
    task_id = create_resp.json()["id"]

    response = await client.post(f"/api/tasks/{task_id}/done", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["completed_at"] is not None


@pytest.mark.asyncio
async def test_mark_task_pending(client: AsyncClient, auth_headers):
    """Test reverting a task to pending."""
    create_resp = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Undo Me"},
    )
    task_id = create_resp.json()["id"]

    # Mark done then pending
    await client.post(f"/api/tasks/{task_id}/done", headers=auth_headers)
    response = await client.post(f"/api/tasks/{task_id}/pending", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["completed_at"] is None


@pytest.mark.asyncio
async def test_task_isolation_between_users(client: AsyncClient, session, auth_headers):
    """Test that users can only access their own tasks."""
    # Create task as test_user
    create_resp = await client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Private Task"},
    )
    task_id = create_resp.json()["id"]

    # Create another user and try to access the task
    from app.services.auth import AuthService
    from app.models.user import UserCreate

    auth_service = AuthService(session)
    other_user = await auth_service.create_user(
        UserCreate(
            email="other@example.com",
            password="otherpassword",
            name="Other User",
        )
    )
    await session.commit()

    other_token = AuthService.create_access_token(other_user.id)
    other_headers = {"Authorization": f"Bearer {other_token}"}

    # Other user should get 404 (task not found for them)
    response = await client.get(f"/api/tasks/{task_id}", headers=other_headers)
    assert response.status_code == 404
