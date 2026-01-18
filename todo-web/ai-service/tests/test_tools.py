"""Tests for MCP tools."""

import pytest
from unittest.mock import AsyncMock, patch

from app.mcp.tools import TodoTools


@pytest.fixture
def tools():
    """Create TodoTools instance."""
    return TodoTools()


@pytest.fixture
def mock_httpx():
    """Mock httpx client."""
    with patch("app.mcp.tools.httpx.AsyncClient") as mock:
        client = AsyncMock()
        mock.return_value.__aenter__.return_value = client
        yield client


@pytest.mark.asyncio
async def test_list_tasks(tools, mock_httpx):
    """Test listing tasks."""
    mock_httpx.request.return_value.json.return_value = [
        {"id": "1", "title": "Task 1"},
        {"id": "2", "title": "Task 2"},
    ]
    mock_httpx.request.return_value.status_code = 200
    mock_httpx.request.return_value.raise_for_status = lambda: None

    result = await tools.list_tasks("test-token")

    assert result["count"] == 2
    assert len(result["tasks"]) == 2
    mock_httpx.request.assert_called_once()


@pytest.mark.asyncio
async def test_create_task(tools, mock_httpx):
    """Test creating a task."""
    mock_httpx.request.return_value.json.return_value = {
        "id": "1",
        "title": "New Task",
        "priority": "high",
    }
    mock_httpx.request.return_value.status_code = 201
    mock_httpx.request.return_value.raise_for_status = lambda: None

    result = await tools.create_task(
        "test-token",
        title="New Task",
        priority="high",
    )

    assert result["task"]["title"] == "New Task"
    assert "Created task" in result["message"]


@pytest.mark.asyncio
async def test_complete_task(tools, mock_httpx):
    """Test completing a task."""
    mock_httpx.request.return_value.json.return_value = {
        "id": "1",
        "title": "Task 1",
        "status": "done",
    }
    mock_httpx.request.return_value.status_code = 200
    mock_httpx.request.return_value.raise_for_status = lambda: None

    result = await tools.complete_task("test-token", "1")

    assert result["task"]["status"] == "done"
    assert "Completed" in result["message"]


@pytest.mark.asyncio
async def test_delete_task(tools, mock_httpx):
    """Test deleting a task."""
    mock_httpx.request.return_value.status_code = 204
    mock_httpx.request.return_value.raise_for_status = lambda: None

    result = await tools.delete_task("test-token", "1")

    assert result["success"] is True
    assert "Deleted" in result["message"]
