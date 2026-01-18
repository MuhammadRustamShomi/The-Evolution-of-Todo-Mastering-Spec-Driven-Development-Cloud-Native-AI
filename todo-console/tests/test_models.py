"""Tests for the Task model."""

from datetime import datetime

import pytest

from models import Task


class TestTask:
    """Tests for the Task dataclass."""

    def test_create_task_with_defaults(self):
        """Task created with minimal args has correct defaults."""
        task = Task(id=1, title="Test task")

        assert task.id == 1
        assert task.title == "Test task"
        assert task.description is None
        assert task.status == "pending"
        assert task.completed_at is None
        assert isinstance(task.created_at, datetime)

    def test_create_task_with_description(self):
        """Task can be created with a description."""
        task = Task(id=1, title="Test", description="Details here")

        assert task.description == "Details here"

    def test_mark_done(self):
        """mark_done() changes status and sets completed_at."""
        task = Task(id=1, title="Test")

        task.mark_done()

        assert task.status == "done"
        assert task.completed_at is not None
        assert isinstance(task.completed_at, datetime)

    def test_mark_pending(self):
        """mark_pending() reverts status and clears completed_at."""
        task = Task(id=1, title="Test")
        task.mark_done()

        task.mark_pending()

        assert task.status == "pending"
        assert task.completed_at is None

    def test_mark_done_then_pending(self):
        """Task can toggle between done and pending."""
        task = Task(id=1, title="Test")

        # Start pending
        assert task.status == "pending"

        # Mark done
        task.mark_done()
        assert task.status == "done"
        assert task.completed_at is not None

        # Back to pending
        task.mark_pending()
        assert task.status == "pending"
        assert task.completed_at is None

        # Done again
        task.mark_done()
        assert task.status == "done"
