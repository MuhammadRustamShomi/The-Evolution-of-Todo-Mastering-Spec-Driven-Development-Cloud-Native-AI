"""Tasks router."""

from datetime import date
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.middleware.auth import get_current_user
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskStatus
from app.models.user import User
from app.services.tasks import TaskService

router = APIRouter()


class TaskListResponse(TaskRead):
    """Task list response with pagination info."""

    pass


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Create a new task."""
    task_service = TaskService(session)
    task = await task_service.create(current_user.id, task_in)
    return TaskRead.model_validate(task)


@router.get("", response_model=list[TaskRead])
async def list_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    due_before: Optional[date] = Query(None, description="Filter tasks due before this date"),
    due_after: Optional[date] = Query(None, description="Filter tasks due after this date"),
    limit: int = Query(100, ge=1, le=1000, description="Number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
):
    """List all tasks for the current user."""
    task_service = TaskService(session)
    tasks = await task_service.list(
        user_id=current_user.id,
        status=status,
        due_before=due_before,
        due_after=due_after,
        limit=limit,
        offset=offset,
    )
    return [TaskRead.model_validate(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Get a specific task by ID."""
    task_service = TaskService(session)
    task = await task_service.get(task_id, current_user.id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Update a task."""
    task_service = TaskService(session)
    task = await task_service.update(task_id, current_user.id, task_in)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Delete a task."""
    task_service = TaskService(session)
    deleted = await task_service.delete(task_id, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.post("/{task_id}/done", response_model=TaskRead)
async def mark_task_done(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Mark a task as done."""
    task_service = TaskService(session)
    task = await task_service.update(
        task_id, current_user.id, TaskUpdate(status=TaskStatus.DONE)
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskRead.model_validate(task)


@router.post("/{task_id}/pending", response_model=TaskRead)
async def mark_task_pending(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Mark a task as pending."""
    task_service = TaskService(session)
    task = await task_service.update(
        task_id, current_user.id, TaskUpdate(status=TaskStatus.PENDING)
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskRead.model_validate(task)
