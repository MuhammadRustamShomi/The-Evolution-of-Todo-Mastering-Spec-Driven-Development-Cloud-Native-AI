#!/usr/bin/env python3
"""Todo Console Application - Phase I of the Todo App Hackathon.

A simple command-line todo application with in-memory storage.
"""

import re
import sys

from commands import CommandHandler
from storage import TaskStorage

WELCOME_MESSAGE = """
╔═══════════════════════════════════════════════════╗
║           Todo Console Application v1.0            ║
║         Type 'help' for available commands         ║
╚═══════════════════════════════════════════════════╝
"""


def parse_command(input_str: str) -> tuple[str, list[str], dict[str, str]]:
    """Parse user input into command, positional args, and named args.

    Examples:
        "add Buy groceries" -> ("add", ["Buy groceries"], {})
        "add Buy groceries --desc Milk and eggs" -> ("add", ["Buy groceries"], {"desc": "Milk and eggs"})
        "list --status pending" -> ("list", [], {"status": "pending"})
    """
    if not input_str.strip():
        return "", [], {}

    # Split into tokens, respecting quotes
    tokens = []
    current_token = ""
    in_quotes = False
    quote_char = None

    for char in input_str:
        if char in "\"'" and not in_quotes:
            in_quotes = True
            quote_char = char
        elif char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
        elif char == " " and not in_quotes:
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    if not tokens:
        return "", [], {}

    command = tokens[0].lower()
    args = []
    kwargs = {}

    i = 1
    positional_done = False

    while i < len(tokens):
        token = tokens[i]
        if token.startswith("--"):
            positional_done = True
            key = token[2:]
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                # Collect all tokens until next flag as the value
                value_parts = []
                i += 1
                while i < len(tokens) and not tokens[i].startswith("--"):
                    value_parts.append(tokens[i])
                    i += 1
                kwargs[key] = " ".join(value_parts)
                continue
            else:
                kwargs[key] = ""
        elif not positional_done:
            args.append(token)
        i += 1

    # Join positional args into a single string for commands like "add"
    positional = " ".join(args) if args else ""

    return command, [positional] if positional else [], kwargs


def run_command(handler: CommandHandler, command: str, args: list[str], kwargs: dict[str, str]) -> str:
    """Execute a parsed command and return the result."""
    try:
        if command == "add":
            title = args[0] if args else ""
            desc = kwargs.get("desc")
            return handler.add(title, desc)

        elif command == "list":
            status = kwargs.get("status")
            return handler.list(status)

        elif command == "show":
            if not args or not args[0]:
                return "Error: Task ID required. Usage: show <id>"
            try:
                task_id = int(args[0])
            except ValueError:
                return "Error: Task ID must be a number."
            return handler.show(task_id)

        elif command == "done":
            if not args or not args[0]:
                return "Error: Task ID required. Usage: done <id>"
            try:
                task_id = int(args[0])
            except ValueError:
                return "Error: Task ID must be a number."
            return handler.done(task_id)

        elif command == "undo":
            if not args or not args[0]:
                return "Error: Task ID required. Usage: undo <id>"
            try:
                task_id = int(args[0])
            except ValueError:
                return "Error: Task ID must be a number."
            return handler.undo(task_id)

        elif command == "delete":
            if not args or not args[0]:
                return "Error: Task ID required. Usage: delete <id>"
            try:
                task_id = int(args[0])
            except ValueError:
                return "Error: Task ID must be a number."
            return handler.delete(task_id)

        elif command == "edit":
            if not args or not args[0]:
                return "Error: Task ID required. Usage: edit <id> [--title <t>] [--desc <d>]"
            try:
                task_id = int(args[0])
            except ValueError:
                return "Error: Task ID must be a number."
            title = kwargs.get("title")
            desc = kwargs.get("desc")
            return handler.edit(task_id, title, desc)

        elif command == "help":
            return handler.help()

        elif command == "exit" or command == "quit":
            return "__EXIT__"

        elif command == "":
            return ""

        else:
            return f"Unknown command: '{command}'. Type 'help' for available commands."

    except Exception as e:
        return f"Error: {e}"


def main() -> None:
    """Main entry point for the todo console application."""
    storage = TaskStorage()
    handler = CommandHandler(storage)

    print(WELCOME_MESSAGE)

    while True:
        try:
            user_input = input("Todo > ").strip()
            command, args, kwargs = parse_command(user_input)
            result = run_command(handler, command, args, kwargs)

            if result == "__EXIT__":
                print("Goodbye!")
                break
            elif result:
                print(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
