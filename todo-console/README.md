# Todo Console App

Phase I of "The Evolution of Todo" - A simple command-line todo application.

## Features

- Add, list, edit, and delete tasks
- Mark tasks as done/pending
- Filter tasks by status
- Interactive REPL interface
- Keyboard shortcuts

## Usage

```bash
# Start the interactive CLI
uv run todo

# Commands
Todo > add Buy groceries
Todo > list
Todo > done 1
Todo > undo 1
Todo > edit 1 --title "Buy more groceries"
Todo > delete 1
Todo > help
Todo > exit
```

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=term-missing
```
