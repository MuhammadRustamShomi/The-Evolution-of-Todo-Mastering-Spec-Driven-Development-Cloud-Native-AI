"""Chat router for AI conversations."""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from app.agent import TodoAgent

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message request."""

    message: str
    conversation_id: Optional[str] = None
    history: Optional[list[dict]] = None


class ChatResponse(BaseModel):
    """Non-streaming chat response."""

    response: str
    conversation_id: str


# In-memory conversation storage (replace with database in production)
conversations: dict[str, list[dict]] = {}


@router.post("/message")
async def chat_message(
    request: ChatMessage,
    authorization: str = Header(...),
):
    """
    Send a message to the AI assistant and get a streaming response.

    Returns a Server-Sent Events stream with the AI's response.
    """
    # Extract token from Authorization header
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization[7:]  # Remove "Bearer " prefix

    # Get or create conversation ID
    conversation_id = request.conversation_id or str(uuid4())

    # Get conversation history
    history = request.history or conversations.get(conversation_id, [])

    # Create agent
    agent = TodoAgent(user_token=token)

    async def generate():
        """Generate SSE events."""
        full_response = ""

        # Send conversation ID first
        yield {
            "event": "conversation_id",
            "data": conversation_id,
        }

        # Stream the response
        async for chunk in agent.chat(request.message, history):
            full_response += chunk
            yield {
                "event": "message",
                "data": chunk,
            }

        # Store the conversation
        history.append({"role": "user", "content": request.message})
        history.append({"role": "assistant", "content": full_response})
        conversations[conversation_id] = history[-20:]  # Keep last 20 messages

        # Send done event
        yield {
            "event": "done",
            "data": "",
        }

    return EventSourceResponse(generate())


@router.get("/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """Get the history of a conversation."""
    history = conversations.get(conversation_id, [])
    return {"conversation_id": conversation_id, "messages": history}


@router.delete("/history/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a conversation's history."""
    if conversation_id in conversations:
        del conversations[conversation_id]
    return {"message": "Conversation cleared"}
