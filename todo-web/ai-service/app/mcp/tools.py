"""MCP Tools for Todo operations."""

from typing import Optional
import httpx

from app.config import get_settings


class TodoTools:
    """Tools for interacting with the Todo API."""

    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.backend_url

    async def _request(
        self,
        method: str,
        endpoint: str,
        token: str,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> dict:
        """Make an authenticated request to the backend."""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.base_url}{endpoint}",
                headers={"Authorization": f"Bearer {token}"},
                json=json,
                params=params,
                timeout=30.0,
            )
            response.raise_for_status()
            if response.status_code == 204:
                return {"success": True}
            return response.json()

    async def list_tasks(
        self,
        token: str,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> dict:
        """
        List user's tasks.

        Args:
            token: User's access token
            status: Filter by status (pending, in_progress, done)
            limit: Maximum number of tasks to return

        Returns:
            List of tasks
        """
        params = {"limit": limit}
        if status:
            params["status"] = status

        tasks = await self._request("GET", "/api/tasks", token, params=params)
        return {
            "tasks": tasks,
            "count": len(tasks),
            "message": f"Found {len(tasks)} tasks",
        }

    async def create_task(
        self,
        token: str,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium",
        due_date: Optional[str] = None,
    ) -> dict:
        """
        Create a new task.

        Args:
            token: User's access token
            title: Task title
            description: Optional task description
            priority: Task priority (low, medium, high)
            due_date: Optional due date in YYYY-MM-DD format

        Returns:
            Created task details
        """
        data = {"title": title, "priority": priority}
        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date

        task = await self._request("POST", "/api/tasks", token, json=data)
        return {
            "task": task,
            "message": f"Created task: {title}",
        }

    async def update_task(
        self,
        token: str,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> dict:
        """
        Update an existing task.

        Args:
            token: User's access token
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            status: New status (optional)
            due_date: New due date (optional)

        Returns:
            Updated task details
        """
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if priority is not None:
            data["priority"] = priority
        if status is not None:
            data["status"] = status
        if due_date is not None:
            data["due_date"] = due_date

        task = await self._request("PATCH", f"/api/tasks/{task_id}", token, json=data)
        return {
            "task": task,
            "message": f"Updated task: {task['title']}",
        }

    async def complete_task(self, token: str, task_id: str) -> dict:
        """
        Mark a task as complete.

        Args:
            token: User's access token
            task_id: ID of the task to complete

        Returns:
            Completed task details
        """
        task = await self._request("POST", f"/api/tasks/{task_id}/done", token)
        return {
            "task": task,
            "message": f"Completed task: {task['title']}",
        }

    async def reopen_task(self, token: str, task_id: str) -> dict:
        """
        Reopen a completed task.

        Args:
            token: User's access token
            task_id: ID of the task to reopen

        Returns:
            Reopened task details
        """
        task = await self._request("POST", f"/api/tasks/{task_id}/pending", token)
        return {
            "task": task,
            "message": f"Reopened task: {task['title']}",
        }

    async def delete_task(self, token: str, task_id: str) -> dict:
        """
        Delete a task.

        Args:
            token: User's access token
            task_id: ID of the task to delete

        Returns:
            Deletion confirmation
        """
        await self._request("DELETE", f"/api/tasks/{task_id}", token)
        return {
            "success": True,
            "message": f"Deleted task {task_id}",
        }

    async def get_task(self, token: str, task_id: str) -> dict:
        """
        Get details of a specific task.

        Args:
            token: User's access token
            task_id: ID of the task

        Returns:
            Task details
        """
        task = await self._request("GET", f"/api/tasks/{task_id}", token)
        return {
            "task": task,
            "message": f"Task: {task['title']}",
        }


# Singleton instance
todo_tools = TodoTools()
