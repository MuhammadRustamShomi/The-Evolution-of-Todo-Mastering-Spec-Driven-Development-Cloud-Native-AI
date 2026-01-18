"""Tests for the CLI parsing and command execution."""

import pytest

from todo import parse_command, run_command
from commands import CommandHandler
from storage import TaskStorage


class TestParseCommand:
    """Tests for command parsing."""

    def test_empty_input(self):
        """Empty input returns empty command."""
        cmd, args, kwargs = parse_command("")
        assert cmd == ""
        assert args == []
        assert kwargs == {}

    def test_simple_command(self):
        """Simple command with no args."""
        cmd, args, kwargs = parse_command("help")
        assert cmd == "help"
        assert args == []
        assert kwargs == {}

    def test_command_with_positional(self):
        """Command with positional argument."""
        cmd, args, kwargs = parse_command("add Buy groceries")
        assert cmd == "add"
        assert args == ["Buy groceries"]
        assert kwargs == {}

    def test_command_with_flag(self):
        """Command with flag argument."""
        cmd, args, kwargs = parse_command("list --status pending")
        assert cmd == "list"
        assert args == []
        assert kwargs == {"status": "pending"}

    def test_command_with_positional_and_flag(self):
        """Command with both positional and flag."""
        cmd, args, kwargs = parse_command("add Buy milk --desc For breakfast")
        assert cmd == "add"
        assert args == ["Buy milk"]
        assert kwargs == {"desc": "For breakfast"}

    def test_quoted_argument(self):
        """Quoted argument is preserved."""
        cmd, args, kwargs = parse_command("add 'Buy groceries today'")
        assert cmd == "add"
        assert args == ["Buy groceries today"]

    def test_multiple_flags(self):
        """Multiple flags are parsed."""
        cmd, args, kwargs = parse_command("edit 1 --title New --desc Updated")
        assert cmd == "edit"
        assert args == ["1"]
        assert kwargs == {"title": "New", "desc": "Updated"}

    def test_case_insensitive_command(self):
        """Command is lowercase."""
        cmd, args, kwargs = parse_command("ADD task")
        assert cmd == "add"


class TestRunCommand:
    """Tests for command execution."""

    @pytest.fixture
    def handler(self):
        """Create fresh handler for each test."""
        return CommandHandler(TaskStorage())

    def test_exit_command(self, handler):
        """exit returns special marker."""
        result = run_command(handler, "exit", [], {})
        assert result == "__EXIT__"

    def test_quit_command(self, handler):
        """quit also exits."""
        result = run_command(handler, "quit", [], {})
        assert result == "__EXIT__"

    def test_unknown_command(self, handler):
        """Unknown command returns error."""
        result = run_command(handler, "invalid", [], {})
        assert "Unknown command" in result

    def test_add_command(self, handler):
        """add command creates task."""
        result = run_command(handler, "add", ["Buy groceries"], {})
        assert "Created task #1" in result

    def test_add_with_desc(self, handler):
        """add command with description."""
        result = run_command(handler, "add", ["Task"], {"desc": "Details"})
        assert "Created task #1" in result
        task = handler.storage.get(1)
        assert task.description == "Details"

    def test_list_command(self, handler):
        """list command shows tasks."""
        handler.add("Task 1")
        result = run_command(handler, "list", [], {})
        assert "Task 1" in result

    def test_done_command(self, handler):
        """done command marks task."""
        handler.add("Task")
        result = run_command(handler, "done", ["1"], {})
        assert "Marked task #1 as done" in result

    def test_done_invalid_id(self, handler):
        """done with non-numeric id."""
        result = run_command(handler, "done", ["abc"], {})
        assert "must be a number" in result

    def test_done_no_id(self, handler):
        """done without id."""
        result = run_command(handler, "done", [], {})
        assert "Task ID required" in result

    def test_undo_command(self, handler):
        """undo command reverts task."""
        handler.add("Task")
        handler.done(1)
        result = run_command(handler, "undo", ["1"], {})
        assert "pending" in result

    def test_delete_command(self, handler):
        """delete command removes task."""
        handler.add("Task")
        result = run_command(handler, "delete", ["1"], {})
        assert "Deleted task #1" in result

    def test_edit_command(self, handler):
        """edit command updates task."""
        handler.add("Original")
        result = run_command(handler, "edit", ["1"], {"title": "Updated"})
        assert "Updated task #1" in result

    def test_show_command(self, handler):
        """show command displays task."""
        handler.add("Test task")
        result = run_command(handler, "show", ["1"], {})
        assert "Task #1" in result
        assert "Test task" in result

    def test_help_command(self, handler):
        """help command shows usage."""
        result = run_command(handler, "help", [], {})
        assert "add" in result
        assert "list" in result

    def test_empty_command(self, handler):
        """Empty command returns empty string."""
        result = run_command(handler, "", [], {})
        assert result == ""
