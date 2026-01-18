"""In-memory storage for todo tasks."""

from typing import Optional

from models import Task, TaskStatus


class TaskStorage:
    """In-memory task storage with CRUD operations."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def create(self, title: str, description: Optional[str] = None) -> Task:
        """Create and store a new task."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def list(self, status: Optional[TaskStatus] = None) -> list[Task]:
        """List tasks with optional status filter."""
        if status is None:
            return self._tasks.copy()
        return [t for t in self._tasks if t.status == status]

    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update task properties."""
        task = self.get(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key) and key not in ("id", "created_at"):
                    setattr(task, key, value)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete task by ID."""
        task = self.get(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def count(self) -> int:
        """Return total number of tasks."""
        return len(self._tasks)
