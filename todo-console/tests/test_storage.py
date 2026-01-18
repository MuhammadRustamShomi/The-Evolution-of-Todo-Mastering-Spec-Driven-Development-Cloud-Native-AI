"""Tests for the TaskStorage class."""

import pytest

from storage import TaskStorage


class TestTaskStorage:
    """Tests for TaskStorage CRUD operations."""

    def test_create_task(self):
        """create() adds task with sequential ID."""
        storage = TaskStorage()

        task1 = storage.create("First task")
        task2 = storage.create("Second task")

        assert task1.id == 1
        assert task1.title == "First task"
        assert task2.id == 2
        assert task2.title == "Second task"

    def test_create_task_with_description(self):
        """create() stores description."""
        storage = TaskStorage()

        task = storage.create("Task", description="Details")

        assert task.description == "Details"

    def test_get_existing_task(self):
        """get() returns task by ID."""
        storage = TaskStorage()
        created = storage.create("Test task")

        found = storage.get(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.title == "Test task"

    def test_get_nonexistent_task(self):
        """get() returns None for missing ID."""
        storage = TaskStorage()

        found = storage.get(999)

        assert found is None

    def test_list_all_tasks(self):
        """list() returns all tasks when no filter."""
        storage = TaskStorage()
        storage.create("Task 1")
        storage.create("Task 2")
        storage.create("Task 3")

        tasks = storage.list()

        assert len(tasks) == 3

    def test_list_empty_storage(self):
        """list() returns empty list when no tasks."""
        storage = TaskStorage()

        tasks = storage.list()

        assert tasks == []

    def test_list_pending_tasks(self):
        """list() filters by pending status."""
        storage = TaskStorage()
        t1 = storage.create("Pending 1")
        t2 = storage.create("Done 1")
        t2.mark_done()
        t3 = storage.create("Pending 2")

        pending = storage.list(status="pending")

        assert len(pending) == 2
        assert all(t.status == "pending" for t in pending)

    def test_list_done_tasks(self):
        """list() filters by done status."""
        storage = TaskStorage()
        t1 = storage.create("Pending 1")
        t2 = storage.create("Done 1")
        t2.mark_done()
        t3 = storage.create("Done 2")
        t3.mark_done()

        done = storage.list(status="done")

        assert len(done) == 2
        assert all(t.status == "done" for t in done)

    def test_update_task_title(self):
        """update() changes task title."""
        storage = TaskStorage()
        task = storage.create("Original")

        storage.update(task.id, title="Updated")

        assert task.title == "Updated"

    def test_update_task_description(self):
        """update() changes task description."""
        storage = TaskStorage()
        task = storage.create("Task")

        storage.update(task.id, description="New description")

        assert task.description == "New description"

    def test_update_nonexistent_task(self):
        """update() returns None for missing ID."""
        storage = TaskStorage()

        result = storage.update(999, title="Test")

        assert result is None

    def test_update_does_not_change_id(self):
        """update() ignores id field."""
        storage = TaskStorage()
        task = storage.create("Task")
        original_id = task.id

        storage.update(task.id, id=999)

        assert task.id == original_id

    def test_delete_existing_task(self):
        """delete() removes task and returns True."""
        storage = TaskStorage()
        task = storage.create("To delete")

        result = storage.delete(task.id)

        assert result is True
        assert storage.get(task.id) is None
        assert storage.count() == 0

    def test_delete_nonexistent_task(self):
        """delete() returns False for missing ID."""
        storage = TaskStorage()

        result = storage.delete(999)

        assert result is False

    def test_count(self):
        """count() returns number of tasks."""
        storage = TaskStorage()

        assert storage.count() == 0

        storage.create("Task 1")
        assert storage.count() == 1

        storage.create("Task 2")
        assert storage.count() == 2

        storage.delete(1)
        assert storage.count() == 1

    def test_list_returns_copy(self):
        """list() returns a copy, not the internal list."""
        storage = TaskStorage()
        storage.create("Task")

        tasks = storage.list()
        tasks.clear()

        assert storage.count() == 1
