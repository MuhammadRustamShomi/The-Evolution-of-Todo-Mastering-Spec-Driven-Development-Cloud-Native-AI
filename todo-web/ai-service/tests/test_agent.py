"""Tests for the AI agent."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.agent.runner import TodoAgent


@pytest.fixture
def mock_openai():
    """Mock OpenAI client."""
    with patch("app.agent.runner.AsyncOpenAI") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture
def agent(mock_openai):
    """Create TodoAgent instance."""
    return TodoAgent("test-token")


@pytest.mark.asyncio
async def test_agent_initialization(agent):
    """Test agent is initialized correctly."""
    assert agent.user_token == "test-token"
    assert agent.model == "gpt-4o"


@pytest.mark.asyncio
async def test_execute_tool_list_tasks(agent):
    """Test executing list_tasks tool."""
    with patch("app.agent.runner.todo_tools") as mock_tools:
        mock_tools.list_tasks = AsyncMock(return_value={
            "tasks": [{"id": "1", "title": "Test"}],
            "count": 1,
            "message": "Found 1 tasks",
        })

        result = await agent._execute_tool("list_tasks", {})

        assert "tasks" in result
        mock_tools.list_tasks.assert_called_once()


@pytest.mark.asyncio
async def test_execute_tool_create_task(agent):
    """Test executing create_task tool."""
    with patch("app.agent.runner.todo_tools") as mock_tools:
        mock_tools.create_task = AsyncMock(return_value={
            "task": {"id": "1", "title": "New Task"},
            "message": "Created task: New Task",
        })

        result = await agent._execute_tool(
            "create_task",
            {"title": "New Task", "priority": "high"},
        )

        assert "task" in result
        mock_tools.create_task.assert_called_once()


@pytest.mark.asyncio
async def test_execute_tool_unknown(agent):
    """Test executing unknown tool returns error."""
    result = await agent._execute_tool("unknown_tool", {})

    assert "error" in result
    assert "Unknown tool" in result
