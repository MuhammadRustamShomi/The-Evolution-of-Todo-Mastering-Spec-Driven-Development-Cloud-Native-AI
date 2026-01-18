"""Agent runner for handling conversations."""

import json
from typing import AsyncGenerator, Optional
from openai import AsyncOpenAI

from app.config import get_settings
from app.agent.config import AGENT_INSTRUCTIONS, TOOL_DEFINITIONS
from app.mcp.tools import todo_tools


class TodoAgent:
    """AI Agent for managing todo tasks."""

    def __init__(self, user_token: str):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        self.model = self.settings.openai_model
        self.user_token = user_token
        self.messages: list[dict] = []

    async def _execute_tool(self, name: str, arguments: dict) -> str:
        """Execute a tool and return the result."""
        try:
            if name == "list_tasks":
                result = await todo_tools.list_tasks(
                    self.user_token,
                    status=arguments.get("status"),
                    limit=arguments.get("limit", 20),
                )
            elif name == "create_task":
                result = await todo_tools.create_task(
                    self.user_token,
                    title=arguments["title"],
                    description=arguments.get("description"),
                    priority=arguments.get("priority", "medium"),
                    due_date=arguments.get("due_date"),
                )
            elif name == "update_task":
                result = await todo_tools.update_task(
                    self.user_token,
                    task_id=arguments["task_id"],
                    title=arguments.get("title"),
                    description=arguments.get("description"),
                    priority=arguments.get("priority"),
                    status=arguments.get("status"),
                    due_date=arguments.get("due_date"),
                )
            elif name == "complete_task":
                result = await todo_tools.complete_task(
                    self.user_token,
                    task_id=arguments["task_id"],
                )
            elif name == "reopen_task":
                result = await todo_tools.reopen_task(
                    self.user_token,
                    task_id=arguments["task_id"],
                )
            elif name == "delete_task":
                result = await todo_tools.delete_task(
                    self.user_token,
                    task_id=arguments["task_id"],
                )
            elif name == "get_task":
                result = await todo_tools.get_task(
                    self.user_token,
                    task_id=arguments["task_id"],
                )
            else:
                result = {"error": f"Unknown tool: {name}"}

            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})

    async def chat(
        self,
        user_message: str,
        conversation_history: Optional[list[dict]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Process a user message and stream the response.

        Args:
            user_message: The user's message
            conversation_history: Previous messages in the conversation

        Yields:
            Response chunks as they're generated
        """
        # Initialize messages with system prompt
        messages = [{"role": "system", "content": AGENT_INSTRUCTIONS}]

        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)

        # Add the new user message
        messages.append({"role": "user", "content": user_message})

        while True:
            # Create streaming completion
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                stream=True,
            )

            # Collect the response
            collected_content = ""
            collected_tool_calls = []
            current_tool_call = None

            async for chunk in stream:
                delta = chunk.choices[0].delta

                # Handle content
                if delta.content:
                    collected_content += delta.content
                    yield delta.content

                # Handle tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        if tool_call.index is not None:
                            # New or continuing tool call
                            while len(collected_tool_calls) <= tool_call.index:
                                collected_tool_calls.append({
                                    "id": "",
                                    "type": "function",
                                    "function": {"name": "", "arguments": ""},
                                })

                            current = collected_tool_calls[tool_call.index]

                            if tool_call.id:
                                current["id"] = tool_call.id
                            if tool_call.function:
                                if tool_call.function.name:
                                    current["function"]["name"] = tool_call.function.name
                                if tool_call.function.arguments:
                                    current["function"]["arguments"] += tool_call.function.arguments

            # If there are tool calls, execute them
            if collected_tool_calls:
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": collected_content if collected_content else None,
                    "tool_calls": collected_tool_calls,
                })

                # Execute each tool and add results
                for tool_call in collected_tool_calls:
                    yield f"\n[Executing: {tool_call['function']['name']}]\n"

                    arguments = json.loads(tool_call["function"]["arguments"])
                    result = await self._execute_tool(
                        tool_call["function"]["name"],
                        arguments,
                    )

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result,
                    })

                # Continue the loop to get the final response
                continue
            else:
                # No more tool calls, we're done
                break

    def get_messages(self) -> list[dict]:
        """Get the current conversation messages."""
        return self.messages
