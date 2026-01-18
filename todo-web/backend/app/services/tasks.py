"""Task service for business logic."""

from datetime import datetime, date
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.task import Task, TaskCreate, TaskUpdate, TaskStatus


class TaskService:
    """Task management service."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, task_in: TaskCreate) -> Task:
        """Create a new task for a user."""
        task = Task(
            user_id=user_id,
            title=task_in.title,
            description=task_in.description,
            priority=task_in.priority,
            due_date=task_in.due_date,
            tags=task_in.tags,
        )
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Get a task by ID, ensuring it belongs to the user."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list(
        self,
        user_id: UUID,
        status: Optional[TaskStatus] = None,
        due_before: Optional[date] = None,
        due_after: Optional[date] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Task]:
        """List tasks for a user with optional filters."""
        statement = select(Task).where(Task.user_id == user_id)

        if status:
            statement = statement.where(Task.status == status)
        if due_before:
            statement = statement.where(Task.due_date <= due_before)
        if due_after:
            statement = statement.where(Task.due_date >= due_after)

        statement = statement.order_by(Task.created_at.desc())
        statement = statement.limit(limit).offset(offset)

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def update(
        self, task_id: UUID, user_id: UUID, task_in: TaskUpdate
    ) -> Optional[Task]:
        """Update a task."""
        task = await self.get(task_id, user_id)
        if not task:
            return None

        update_data = task_in.model_dump(exclude_unset=True)

        # Handle status changes
        if "status" in update_data:
            if update_data["status"] == TaskStatus.DONE and task.status != TaskStatus.DONE:
                update_data["completed_at"] = datetime.utcnow()
            elif update_data["status"] != TaskStatus.DONE:
                update_data["completed_at"] = None

        update_data["updated_at"] = datetime.utcnow()

        for key, value in update_data.items():
            setattr(task, key, value)

        await self.session.flush()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: UUID, user_id: UUID) -> bool:
        """Delete a task."""
        task = await self.get(task_id, user_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.flush()
        return True

    async def count(self, user_id: UUID, status: Optional[TaskStatus] = None) -> int:
        """Count tasks for a user."""
        from sqlalchemy import func

        statement = select(func.count()).select_from(Task).where(Task.user_id == user_id)
        if status:
            statement = statement.where(Task.status == status)

        result = await self.session.execute(statement)
        return result.scalar_one()
