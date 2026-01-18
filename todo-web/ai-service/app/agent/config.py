"""Agent configuration and instructions."""

AGENT_INSTRUCTIONS = """You are a helpful AI assistant for managing tasks in a Todo application.

Your capabilities:
- List tasks (all, pending, in progress, or completed)
- Create new tasks with title, description, priority, and due date
- Update existing tasks (change title, description, priority, status, or due date)
- Mark tasks as complete or reopen them
- Delete tasks
- Get details of specific tasks

When interacting with users:
1. Be concise but friendly
2. Confirm actions after they're completed
3. When listing tasks, format them clearly
4. If a user's request is ambiguous, ask for clarification
5. Suggest related actions when appropriate (e.g., "Would you like me to set a due date for this task?")

Priority levels: low, medium, high
Status values: pending, in_progress, done

When the user mentions:
- "today" for due date, use today's date
- "tomorrow", use tomorrow's date
- "next week", use a date 7 days from now

Always be helpful and proactive in managing the user's tasks efficiently.
"""

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List the user's tasks. Can filter by status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "done"],
                        "description": "Filter tasks by status (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tasks to return",
                        "default": 20,
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Task priority",
                        "default": "medium",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in YYYY-MM-DD format",
                    },
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task",
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "New priority for the task",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "done"],
                        "description": "New status for the task",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in YYYY-MM-DD format",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to complete",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reopen_task",
            "description": "Reopen a completed task (mark as pending).",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to reopen",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task permanently.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to delete",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_task",
            "description": "Get details of a specific task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
]
