"""Output formatting for task display."""

from models import Task


def truncate(text: str, max_length: int = 30) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_task_table(tasks: list[Task]) -> str:
    """Format tasks as a table for display."""
    if not tasks:
        return "No tasks found."

    # Column widths
    id_width = 4
    title_width = 30
    status_width = 10
    date_width = 12

    # Header
    header = (
        f"{'ID':<{id_width}} | "
        f"{'Title':<{title_width}} | "
        f"{'Status':<{status_width}} | "
        f"{'Created':<{date_width}}"
    )
    separator = "-" * len(header)

    # Rows
    rows = []
    for task in tasks:
        title = truncate(task.title, title_width)
        created = task.created_at.strftime("%Y-%m-%d")
        row = (
            f"{task.id:<{id_width}} | "
            f"{title:<{title_width}} | "
            f"{task.status:<{status_width}} | "
            f"{created:<{date_width}}"
        )
        rows.append(row)

    return "\n".join([header, separator] + rows)


def format_task_detail(task: Task) -> str:
    """Format a single task with all details."""
    lines = [
        f"Task #{task.id}",
        f"  Title: {task.title}",
        f"  Status: {task.status}",
        f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}",
    ]
    if task.description:
        lines.append(f"  Description: {task.description}")
    if task.completed_at:
        lines.append(f"  Completed: {task.completed_at.strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(lines)
