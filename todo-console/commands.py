"""Command handlers for the todo CLI."""

from typing import Optional

from formatter import format_task_table
from storage import TaskStorage


class CommandHandler:
    """Handles CLI command execution."""

    def __init__(self, storage: TaskStorage) -> None:
        self.storage = storage

    def add(self, title: str, desc: Optional[str] = None) -> str:
        """Handle 'add' command - create a new task."""
        if not title or not title.strip():
            return "Error: Task title cannot be empty."
        task = self.storage.create(title.strip(), desc)
        return f"Created task #{task.id}: {task.title}"

    def list(self, status: Optional[str] = None) -> str:
        """Handle 'list' command - display tasks."""
        # Validate status filter
        if status and status not in ("pending", "done", "all"):
            return "Error: Status must be 'pending', 'done', or 'all'."

        # Get tasks with optional filter
        filter_status = None if status == "all" else status
        tasks = self.storage.list(filter_status)  # type: ignore

        return format_task_table(tasks)

    def done(self, task_id: int) -> str:
        """Handle 'done' command - mark task as complete."""
        task = self.storage.get(task_id)
        if not task:
            return f"Error: Task {task_id} not found."
        if task.status == "done":
            return f"Task #{task_id} is already done."
        task.mark_done()
        return f"Marked task #{task_id} as done."

    def undo(self, task_id: int) -> str:
        """Handle 'undo' command - revert task to pending."""
        task = self.storage.get(task_id)
        if not task:
            return f"Error: Task {task_id} not found."
        if task.status == "pending":
            return f"Task #{task_id} is already pending."
        task.mark_pending()
        return f"Marked task #{task_id} as pending."

    def delete(self, task_id: int) -> str:
        """Handle 'delete' command - remove a task."""
        if self.storage.delete(task_id):
            return f"Deleted task #{task_id}."
        return f"Error: Task {task_id} not found."

    def edit(
        self,
        task_id: int,
        title: Optional[str] = None,
        desc: Optional[str] = None,
    ) -> str:
        """Handle 'edit' command - update task properties."""
        task = self.storage.get(task_id)
        if not task:
            return f"Error: Task {task_id} not found."

        updates = {}
        if title is not None:
            if not title.strip():
                return "Error: Task title cannot be empty."
            updates["title"] = title.strip()
        if desc is not None:
            updates["description"] = desc if desc.strip() else None

        if not updates:
            return "Error: No updates provided. Use --title or --desc."

        self.storage.update(task_id, **updates)
        return f"Updated task #{task_id}."

    def show(self, task_id: int) -> str:
        """Handle 'show' command - display task details."""
        from formatter import format_task_detail

        task = self.storage.get(task_id)
        if not task:
            return f"Error: Task {task_id} not found."
        return format_task_detail(task)

    def help(self) -> str:
        """Handle 'help' command - show available commands."""
        return """Available commands:
  add <title> [--desc <description>]  Create a new task
  list [--status pending|done|all]    List tasks
  show <id>                           Show task details
  done <id>                           Mark task as complete
  undo <id>                           Revert task to pending
  edit <id> [--title <t>] [--desc <d>] Update task
  delete <id>                         Delete a task
  help                                Show this help message
  exit                                Exit the application"""
