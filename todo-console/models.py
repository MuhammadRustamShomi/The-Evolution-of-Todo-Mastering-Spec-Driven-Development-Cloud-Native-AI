"""Task data model for the todo console application."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional

TaskStatus = Literal["pending", "done"]


@dataclass
class Task:
    """Represents a todo task with status tracking."""

    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def mark_done(self) -> None:
        """Mark the task as completed."""
        self.status = "done"
        self.completed_at = datetime.now()

    def mark_pending(self) -> None:
        """Revert the task to pending status."""
        self.status = "pending"
        self.completed_at = None
