"""Task model for todo items."""

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Column, ARRAY, String


class TaskStatus(str, Enum):
    """Task status options."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    """Base task fields."""

    title: str = Field(max_length=200)
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))


class Task(TaskBase, table=True):
    """Task database model."""

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class TaskCreate(SQLModel):
    """Task creation schema."""

    title: str = Field(max_length=200)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)


class TaskRead(TaskBase):
    """Task response schema."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]


class TaskUpdate(SQLModel):
    """Task update schema."""

    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None
