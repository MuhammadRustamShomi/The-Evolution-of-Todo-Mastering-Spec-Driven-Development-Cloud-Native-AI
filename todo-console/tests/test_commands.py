"""Tests for the CommandHandler class."""

import pytest

from commands import CommandHandler
from storage import TaskStorage


class TestCommandHandler:
    """Tests for CLI command handlers."""

    @pytest.fixture
    def handler(self):
        """Create a fresh handler for each test."""
        storage = TaskStorage()
        return CommandHandler(storage)

    # Add command tests
    def test_add_task(self, handler):
        """add() creates task and returns confirmation."""
        result = handler.add("Buy groceries")

        assert "Created task #1" in result
        assert "Buy groceries" in result
        assert handler.storage.count() == 1

    def test_add_task_with_description(self, handler):
        """add() stores description."""
        handler.add("Task", desc="Some details")

        task = handler.storage.get(1)
        assert task.description == "Some details"

    def test_add_empty_title(self, handler):
        """add() rejects empty title."""
        result = handler.add("")

        assert "Error" in result
        assert handler.storage.count() == 0

    def test_add_whitespace_title(self, handler):
        """add() rejects whitespace-only title."""
        result = handler.add("   ")

        assert "Error" in result
        assert handler.storage.count() == 0

    # List command tests
    def test_list_empty(self, handler):
        """list() shows message when no tasks."""
        result = handler.list()

        assert "No tasks found" in result

    def test_list_all_tasks(self, handler):
        """list() shows all tasks."""
        handler.add("Task 1")
        handler.add("Task 2")

        result = handler.list()

        assert "Task 1" in result
        assert "Task 2" in result

    def test_list_pending_filter(self, handler):
        """list() filters by pending status."""
        handler.add("Pending task")
        handler.add("Done task")
        handler.done(2)

        result = handler.list(status="pending")

        assert "Pending task" in result
        assert "Done task" not in result

    def test_list_done_filter(self, handler):
        """list() filters by done status."""
        handler.add("Pending task")
        handler.add("Done task")
        handler.done(2)

        result = handler.list(status="done")

        assert "Done task" in result
        assert "Pending task" not in result

    def test_list_all_filter(self, handler):
        """list() with 'all' shows everything."""
        handler.add("Pending task")
        handler.add("Done task")
        handler.done(2)

        result = handler.list(status="all")

        assert "Pending task" in result
        assert "Done task" in result

    def test_list_invalid_status(self, handler):
        """list() rejects invalid status."""
        result = handler.list(status="invalid")

        assert "Error" in result

    # Done command tests
    def test_done_marks_complete(self, handler):
        """done() marks task as complete."""
        handler.add("Task")

        result = handler.done(1)

        assert "Marked task #1 as done" in result
        task = handler.storage.get(1)
        assert task.status == "done"

    def test_done_already_done(self, handler):
        """done() reports if already complete."""
        handler.add("Task")
        handler.done(1)

        result = handler.done(1)

        assert "already done" in result

    def test_done_nonexistent(self, handler):
        """done() reports missing task."""
        result = handler.done(999)

        assert "Error" in result
        assert "not found" in result

    # Undo command tests
    def test_undo_reverts_pending(self, handler):
        """undo() reverts task to pending."""
        handler.add("Task")
        handler.done(1)

        result = handler.undo(1)

        assert "Marked task #1 as pending" in result
        task = handler.storage.get(1)
        assert task.status == "pending"

    def test_undo_already_pending(self, handler):
        """undo() reports if already pending."""
        handler.add("Task")

        result = handler.undo(1)

        assert "already pending" in result

    def test_undo_nonexistent(self, handler):
        """undo() reports missing task."""
        result = handler.undo(999)

        assert "Error" in result
        assert "not found" in result

    # Delete command tests
    def test_delete_removes_task(self, handler):
        """delete() removes task."""
        handler.add("Task")

        result = handler.delete(1)

        assert "Deleted task #1" in result
        assert handler.storage.count() == 0

    def test_delete_nonexistent(self, handler):
        """delete() reports missing task."""
        result = handler.delete(999)

        assert "Error" in result
        assert "not found" in result

    # Edit command tests
    def test_edit_title(self, handler):
        """edit() updates title."""
        handler.add("Original")

        result = handler.edit(1, title="Updated")

        assert "Updated task #1" in result
        task = handler.storage.get(1)
        assert task.title == "Updated"

    def test_edit_description(self, handler):
        """edit() updates description."""
        handler.add("Task")

        result = handler.edit(1, desc="New description")

        task = handler.storage.get(1)
        assert task.description == "New description"

    def test_edit_both(self, handler):
        """edit() updates title and description."""
        handler.add("Original")

        handler.edit(1, title="New title", desc="New desc")

        task = handler.storage.get(1)
        assert task.title == "New title"
        assert task.description == "New desc"

    def test_edit_empty_title(self, handler):
        """edit() rejects empty title."""
        handler.add("Original")

        result = handler.edit(1, title="")

        assert "Error" in result
        task = handler.storage.get(1)
        assert task.title == "Original"

    def test_edit_no_updates(self, handler):
        """edit() requires at least one update."""
        handler.add("Task")

        result = handler.edit(1)

        assert "Error" in result
        assert "No updates" in result

    def test_edit_nonexistent(self, handler):
        """edit() reports missing task."""
        result = handler.edit(999, title="Test")

        assert "Error" in result
        assert "not found" in result

    # Show command tests
    def test_show_task(self, handler):
        """show() displays task details."""
        handler.add("Test task", desc="Details")

        result = handler.show(1)

        assert "Task #1" in result
        assert "Test task" in result
        assert "Details" in result

    def test_show_nonexistent(self, handler):
        """show() reports missing task."""
        result = handler.show(999)

        assert "Error" in result
        assert "not found" in result

    # Help command tests
    def test_help(self, handler):
        """help() returns command list."""
        result = handler.help()

        assert "add" in result
        assert "list" in result
        assert "done" in result
        assert "delete" in result
        assert "edit" in result
        assert "help" in result
        assert "exit" in result
