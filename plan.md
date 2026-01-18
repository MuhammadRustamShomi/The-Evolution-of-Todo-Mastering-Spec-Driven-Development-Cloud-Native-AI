# Todo App - Technical Plan

## Executive Summary

This plan outlines the technical architecture for a progressively evolving Todo application across five phases:

| Phase | Architecture Style | Key Technologies |
|-------|-------------------|------------------|
| I | CLI Monolith | Python, in-memory storage |
| II | Client-Server | FastAPI, Next.js, Neon, Better Auth |
| III | AI-Augmented | OpenAI Agents SDK, MCP Server |
| IV | Containerized | Docker, Minikube, Helm |
| V | Cloud-Native | Managed K8s, Kafka, Dapr |

**Key Principle**: Each phase builds upon the previous, maintaining backward compatibility while introducing new capabilities.

---

## Phase I: Console Application

### Architecture Overview

```
┌────────────────────────────────────────────────────────────┐
│                     Console Application                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    CLI Interface                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │   Parser    │  │  Commands   │  │  Formatter  │   │  │
│  │  │ (argparse)  │  │   Handler   │  │  (Tables)   │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  └──────────────────────────┬───────────────────────────┘  │
│                             │                               │
│  ┌──────────────────────────▼───────────────────────────┐  │
│  │                   Task Manager                        │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │   Create    │  │   Update    │  │   Delete    │   │  │
│  │  │   Read      │  │   Filter    │  │   Search    │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  └──────────────────────────┬───────────────────────────┘  │
│                             │                               │
│  ┌──────────────────────────▼───────────────────────────┐  │
│  │                 In-Memory Storage                     │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  List[Task] - Sequential ID, O(n) operations   │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.13+ | Core application |
| CLI Parsing | argparse (stdlib) | Command parsing |
| Output | tabulate | Table formatting |
| Types | dataclasses, typing | Type safety |

### Project Structure

```
todo-console/
├── todo.py              # Entry point and main loop
├── models.py            # Task dataclass
├── storage.py           # In-memory task storage
├── commands.py          # Command handlers
├── formatter.py         # Output formatting
├── tests/
│   ├── test_commands.py
│   ├── test_storage.py
│   └── test_models.py
├── pyproject.toml       # Project configuration
└── README.md
```

### Data Model

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Literal

TaskStatus = Literal["pending", "done"]

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def mark_done(self) -> None:
        self.status = "done"
        self.completed_at = datetime.now()

    def mark_pending(self) -> None:
        self.status = "pending"
        self.completed_at = None
```

### Component Details

#### Storage Layer

```python
class TaskStorage:
    """In-memory task storage with CRUD operations."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def create(self, title: str, description: Optional[str] = None) -> Task:
        """Create and store a new task."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def list(self, status: Optional[TaskStatus] = None) -> list[Task]:
        """List tasks with optional status filter."""
        if status is None:
            return self._tasks.copy()
        return [t for t in self._tasks if t.status == status]

    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update task properties."""
        task = self.get(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete task by ID."""
        task = self.get(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False
```

#### Command Handler

```python
class CommandHandler:
    """Handles CLI command execution."""

    def __init__(self, storage: TaskStorage) -> None:
        self.storage = storage

    def add(self, title: str, desc: Optional[str] = None) -> str:
        """Handle 'add' command."""
        task = self.storage.create(title, desc)
        return f"Created task #{task.id}: {task.title}"

    def list(self, status: Optional[str] = None) -> str:
        """Handle 'list' command."""
        tasks = self.storage.list(status)
        if not tasks:
            return "No tasks found."
        return format_task_table(tasks)

    def done(self, task_id: int) -> str:
        """Handle 'done' command."""
        task = self.storage.get(task_id)
        if not task:
            return f"Task {task_id} not found."
        task.mark_done()
        return f"Marked task #{task_id} as done."

    def undo(self, task_id: int) -> str:
        """Handle 'undo' command."""
        task = self.storage.get(task_id)
        if not task:
            return f"Task {task_id} not found."
        task.mark_pending()
        return f"Marked task #{task_id} as pending."

    def delete(self, task_id: int) -> str:
        """Handle 'delete' command."""
        if self.storage.delete(task_id):
            return f"Deleted task #{task_id}."
        return f"Task {task_id} not found."

    def edit(self, task_id: int, title: Optional[str] = None,
             desc: Optional[str] = None) -> str:
        """Handle 'edit' command."""
        updates = {}
        if title:
            updates['title'] = title
        if desc:
            updates['description'] = desc
        task = self.storage.update(task_id, **updates)
        if task:
            return f"Updated task #{task_id}."
        return f"Task {task_id} not found."
```

---

## Phase II: Web Application

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Client Layer                                │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      Next.js 15+ Frontend                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │  │
│  │  │   Pages     │  │ Components  │  │    Client State         │   │  │
│  │  │  (Routes)   │  │   (UI Kit)  │  │  (React Query/SWR)      │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ HTTPS
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              API Layer                                   │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      FastAPI Backend                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │  │
│  │  │   Routers   │  │   Models    │  │      Services           │   │  │
│  │  │  (Endpoints)│  │  (Pydantic) │  │   (Business Logic)      │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │  │
│  │                                                                    │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │  │
│  │  │ Better Auth │  │  SQLModel   │  │     Middleware          │   │  │
│  │  │   (Auth)    │  │   (ORM)     │  │  (CORS, Rate Limit)     │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ SQL
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            Data Layer                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                   Neon Serverless PostgreSQL                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │  │
│  │  │   users     │  │   tasks     │  │     sessions            │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 15+ (App Router) | React framework |
| **Styling** | Tailwind CSS | Utility-first CSS |
| **State** | TanStack Query | Server state management |
| **Forms** | React Hook Form + Zod | Form handling & validation |
| **Backend** | FastAPI | Python API framework |
| **ORM** | SQLModel | Type-safe ORM |
| **Auth** | Better Auth | Authentication library |
| **Database** | Neon | Serverless PostgreSQL |
| **Migrations** | Alembic | Database migrations |

### Project Structure

```
todo-web/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry
│   │   ├── config.py            # Settings
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User model
│   │   │   └── task.py          # Task model
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Auth endpoints
│   │   │   └── tasks.py         # Task endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Auth service
│   │   │   └── tasks.py         # Task service
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── session.py       # DB session
│   │   │   └── migrations/      # Alembic migrations
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── auth.py          # Auth middleware
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   └── (dashboard)/
│   │   │       ├── layout.tsx
│   │   │       ├── today/
│   │   │       ├── upcoming/
│   │   │       └── tasks/
│   │   ├── components/
│   │   │   ├── ui/              # Shadcn/ui components
│   │   │   ├── task/
│   │   │   │   ├── task-card.tsx
│   │   │   │   ├── task-form.tsx
│   │   │   │   └── task-list.tsx
│   │   │   └── layout/
│   │   │       ├── sidebar.tsx
│   │   │       └── header.tsx
│   │   ├── lib/
│   │   │   ├── api.ts           # API client
│   │   │   ├── auth.ts          # Auth utilities
│   │   │   └── utils.ts
│   │   └── types/
│   │       └── index.ts
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

### Database Schema

```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'done')),
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    due_date DATE,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_priority ON tasks(priority);
```

### API Design

#### Authentication Endpoints

```yaml
POST /api/auth/register:
  requestBody:
    email: string
    password: string
    name: string
  responses:
    201: { user: User, token: string }
    400: { error: "Email already exists" }

POST /api/auth/login:
  requestBody:
    email: string
    password: string
  responses:
    200: { user: User, accessToken: string, refreshToken: string }
    401: { error: "Invalid credentials" }

POST /api/auth/refresh:
  headers:
    Authorization: Bearer <refreshToken>
  responses:
    200: { accessToken: string }
    401: { error: "Invalid refresh token" }

POST /api/auth/logout:
  headers:
    Authorization: Bearer <accessToken>
  responses:
    200: { message: "Logged out" }
```

#### Task Endpoints

```yaml
GET /api/tasks:
  headers:
    Authorization: Bearer <token>
  queryParams:
    status: pending | done | all
    priority: low | medium | high
    due_before: ISO date
    tags: comma-separated
    page: number
    limit: number (max 100)
  responses:
    200: { tasks: Task[], total: number, page: number }

POST /api/tasks:
  headers:
    Authorization: Bearer <token>
  requestBody:
    title: string (required)
    description: string
    priority: low | medium | high
    due_date: ISO date
    tags: string[]
  responses:
    201: { task: Task }
    400: { error: "Validation error" }

GET /api/tasks/:id:
  responses:
    200: { task: Task }
    404: { error: "Task not found" }

PATCH /api/tasks/:id:
  requestBody:
    title: string
    description: string
    status: pending | in_progress | done
    priority: low | medium | high
    due_date: ISO date
    tags: string[]
  responses:
    200: { task: Task }
    404: { error: "Task not found" }

DELETE /api/tasks/:id:
  responses:
    200: { message: "Task deleted" }
    404: { error: "Task not found" }
```

### Backend Components

#### SQLModel Task Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)

class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None
```

#### Task Service

```python
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.models.task import Task, TaskCreate, TaskUpdate, TaskStatus

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, user_id: UUID, task_in: TaskCreate) -> Task:
        task = Task(user_id=user_id, **task_in.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await self.session.exec(statement)
        return result.first()

    async def list(
        self,
        user_id: UUID,
        status: Optional[TaskStatus] = None,
        limit: int = 20,
        offset: int = 0
    ) -> list[Task]:
        statement = select(Task).where(Task.user_id == user_id)
        if status:
            statement = statement.where(Task.status == status)
        statement = statement.offset(offset).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def update(
        self,
        task_id: UUID,
        user_id: UUID,
        task_in: TaskUpdate
    ) -> Optional[Task]:
        task = await self.get(task_id, user_id)
        if not task:
            return None

        update_data = task_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.utcnow()

        if task_in.status == TaskStatus.DONE:
            task.completed_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: UUID, user_id: UUID) -> bool:
        task = await self.get(task_id, user_id)
        if not task:
            return False
        await self.session.delete(task)
        await self.session.commit()
        return True
```

### Frontend Components

#### Task List Component

```typescript
'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { Task, TaskStatus } from '@/types'
import { TaskCard } from './task-card'
import { TaskListSkeleton } from './task-list-skeleton'

interface TaskListProps {
  status?: TaskStatus
  date?: 'today' | 'upcoming'
}

export function TaskList({ status, date }: TaskListProps) {
  const queryClient = useQueryClient()

  const { data: tasks, isLoading, error } = useQuery({
    queryKey: ['tasks', { status, date }],
    queryFn: () => api.getTasks({ status, date })
  })

  const toggleMutation = useMutation({
    mutationFn: (task: Task) =>
      api.updateTask(task.id, {
        status: task.status === 'done' ? 'pending' : 'done'
      }),
    onMutate: async (task) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['tasks'] })
      const previous = queryClient.getQueryData(['tasks'])
      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map(t => t.id === task.id
          ? { ...t, status: t.status === 'done' ? 'pending' : 'done' }
          : t
        )
      )
      return { previous }
    },
    onError: (err, task, context) => {
      queryClient.setQueryData(['tasks'], context?.previous)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    }
  })

  if (isLoading) return <TaskListSkeleton />
  if (error) return <div>Failed to load tasks</div>
  if (!tasks?.length) return <EmptyState />

  return (
    <div className="space-y-2">
      {tasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={() => toggleMutation.mutate(task)}
        />
      ))}
    </div>
  )
}
```

---

## Phase III: AI Chatbot

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Chat Interface                                 │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    Next.js Chat Component                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │  │
│  │  │   Message   │  │    Input    │  │     Streaming           │   │  │
│  │  │   History   │  │    Field    │  │     Response            │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ WebSocket/SSE
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Agent Layer                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                   OpenAI Agents SDK                                │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │  │
│  │  │   Agent     │  │   Tools     │  │     Context             │   │  │
│  │  │   Runner    │  │  Registry   │  │     Manager             │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                       MCP Server                                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │  │
│  │  │create_task  │  │ list_tasks  │  │    update_task          │   │  │
│  │  │delete_task  │  │ get_task    │  │    search_tasks         │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                          ┌──────────┴──────────┐
                          ▼                     ▼
              ┌─────────────────┐    ┌─────────────────┐
              │   Task API      │    │   OpenAI API    │
              │   (FastAPI)     │    │   (LLM)         │
              └─────────────────┘    └─────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Agent** | OpenAI Agents SDK | AI agent orchestration |
| **Protocol** | MCP (Model Context Protocol) | Tool integration |
| **Streaming** | Server-Sent Events | Real-time responses |
| **State** | Neon PostgreSQL | Conversation persistence |

### MCP Server Implementation

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel
from typing import Optional
from datetime import date

# Initialize MCP server
server = Server("todo-mcp")

class CreateTaskArgs(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = "medium"
    tags: Optional[list[str]] = None

class ListTasksArgs(BaseModel):
    status: Optional[str] = "all"
    priority: Optional[str] = None
    due_before: Optional[date] = None

class UpdateTaskArgs(BaseModel):
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None

class DeleteTaskArgs(BaseModel):
    task_id: str

# Register tools
@server.tool("create_task")
async def create_task(args: CreateTaskArgs) -> list[TextContent]:
    """Create a new todo task."""
    task = await task_service.create(
        user_id=get_current_user_id(),
        task_in=TaskCreate(**args.model_dump())
    )
    return [TextContent(
        type="text",
        text=f"Created task '{task.title}' (ID: {task.id})"
    )]

@server.tool("list_tasks")
async def list_tasks(args: ListTasksArgs) -> list[TextContent]:
    """List tasks with optional filters."""
    tasks = await task_service.list(
        user_id=get_current_user_id(),
        status=args.status,
        priority=args.priority
    )
    if not tasks:
        return [TextContent(type="text", text="No tasks found.")]

    result = "Your tasks:\n"
    for task in tasks:
        status_icon = "[x]" if task.status == "done" else "[ ]"
        result += f"{status_icon} {task.title}"
        if task.due_date:
            result += f" (due: {task.due_date})"
        result += "\n"

    return [TextContent(type="text", text=result)]

@server.tool("update_task")
async def update_task(args: UpdateTaskArgs) -> list[TextContent]:
    """Update an existing task."""
    task = await task_service.update(
        task_id=args.task_id,
        user_id=get_current_user_id(),
        task_in=TaskUpdate(**args.model_dump(exclude={'task_id'}))
    )
    if not task:
        return [TextContent(type="text", text=f"Task {args.task_id} not found.")]
    return [TextContent(type="text", text=f"Updated task '{task.title}'")]

@server.tool("delete_task")
async def delete_task(args: DeleteTaskArgs) -> list[TextContent]:
    """Delete a task."""
    success = await task_service.delete(
        task_id=args.task_id,
        user_id=get_current_user_id()
    )
    if success:
        return [TextContent(type="text", text=f"Deleted task {args.task_id}")]
    return [TextContent(type="text", text=f"Task {args.task_id} not found.")]
```

### Agent Configuration

```python
from openai import OpenAI
from agents import Agent, Runner

# Define the Todo Agent
todo_agent = Agent(
    name="Todo Assistant",
    model="gpt-4o",
    instructions="""You are a helpful task management assistant. You help users:
    - Create, update, and delete tasks
    - List and search tasks
    - Set due dates and priorities
    - Track task completion

    Guidelines:
    - Be concise and friendly
    - Confirm actions taken
    - Ask for clarification when needed
    - Suggest due dates when not specified
    - Infer priority from language (e.g., "urgent" = high)
    """,
    tools=[
        {"type": "mcp", "server": "todo-mcp"}
    ]
)

# Initialize runner
client = OpenAI()
runner = Runner(client=client)

async def chat(user_message: str, conversation_id: str) -> AsyncGenerator[str, None]:
    """Process user message and stream response."""
    # Load conversation history
    history = await load_conversation(conversation_id)

    # Run agent
    async for event in runner.run_stream(
        agent=todo_agent,
        messages=history + [{"role": "user", "content": user_message}]
    ):
        if event.type == "text_delta":
            yield event.delta
        elif event.type == "tool_call":
            # Tool calls are handled automatically
            pass

    # Save updated conversation
    await save_conversation(conversation_id, runner.messages)
```

### Chat Endpoint

```python
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/chat")

@router.post("/message")
async def send_message(
    request: Request,
    message: str,
    conversation_id: Optional[str] = None
) -> StreamingResponse:
    """Send a message to the AI assistant."""
    user = await get_current_user(request)

    if not conversation_id:
        conversation_id = str(uuid4())

    async def generate():
        async for chunk in chat(message, conversation_id):
            yield f"data: {json.dumps({'text': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "X-Conversation-ID": conversation_id
        }
    )
```

---

## Phase IV: Local Kubernetes

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Minikube Cluster                               │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                         Ingress Controller                          │ │
│  │                    (NGINX Ingress Controller)                       │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│           ┌────────────────────────┼────────────────────────┐           │
│           ▼                        ▼                        ▼           │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐   │
│  │    Frontend     │     │    Backend      │     │   AI Service    │   │
│  │   Deployment    │     │   Deployment    │     │   Deployment    │   │
│  │  ┌───────────┐  │     │  ┌───────────┐  │     │  ┌───────────┐  │   │
│  │  │  Pod 1    │  │     │  │  Pod 1    │  │     │  │  Pod 1    │  │   │
│  │  │ (Next.js) │  │     │  │ (FastAPI) │  │     │  │  (Agent)  │  │   │
│  │  └───────────┘  │     │  └───────────┘  │     │  └───────────┘  │   │
│  │  ┌───────────┐  │     │  ┌───────────┐  │     │                 │   │
│  │  │  Pod 2    │  │     │  │  Pod 2    │  │     │                 │   │
│  │  └───────────┘  │     │  └───────────┘  │     │                 │   │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘   │
│           │                       │                       │             │
│           └───────────────────────┼───────────────────────┘             │
│                                   ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                        Services (ClusterIP)                         │ │
│  │   frontend-svc:80  │  backend-svc:8000  │  ai-svc:8001             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │    ConfigMap     │  │     Secret       │  │   PersistentVolume   │  │
│  │   (App Config)   │  │  (DB Creds, JWT) │  │    (Data Storage)    │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Helm Chart Structure

```
charts/
└── todo/
    ├── Chart.yaml
    ├── values.yaml
    ├── values-dev.yaml
    ├── values-prod.yaml
    ├── templates/
    │   ├── _helpers.tpl
    │   ├── NOTES.txt
    │   ├── frontend/
    │   │   ├── deployment.yaml
    │   │   ├── service.yaml
    │   │   └── hpa.yaml
    │   ├── backend/
    │   │   ├── deployment.yaml
    │   │   ├── service.yaml
    │   │   └── hpa.yaml
    │   ├── ai-service/
    │   │   ├── deployment.yaml
    │   │   └── service.yaml
    │   ├── ingress.yaml
    │   ├── configmap.yaml
    │   └── secrets.yaml
    └── charts/
        └── postgresql/  # Subchart for local DB
```

### Values Configuration

```yaml
# values.yaml
global:
  environment: development
  domain: todo.local

frontend:
  replicaCount: 2
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  resources:
    limits:
      memory: 128Mi
      cpu: 100m
    requests:
      memory: 64Mi
      cpu: 50m
  service:
    type: ClusterIP
    port: 80

backend:
  replicaCount: 2
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  resources:
    limits:
      memory: 256Mi
      cpu: 250m
    requests:
      memory: 128Mi
      cpu: 100m
  service:
    type: ClusterIP
    port: 8000
  env:
    DATABASE_URL: "postgresql://..."
    JWT_SECRET: ""  # Set via secret

aiService:
  enabled: true
  replicaCount: 1
  image:
    repository: todo-ai
    tag: latest
  resources:
    limits:
      memory: 512Mi
      cpu: 500m
  env:
    OPENAI_API_KEY: ""  # Set via secret

ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
          backend: frontend
        - path: /api
          pathType: Prefix
          backend: backend
        - path: /api/chat
          pathType: Prefix
          backend: aiService

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### Deployment Templates

```yaml
# templates/backend/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo.fullname" . }}-backend
  labels:
    {{- include "todo.labels" . | nindent 4 }}
    app.kubernetes.io/component: backend
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: backend
  template:
    metadata:
      labels:
        {{- include "todo.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: backend
    spec:
      containers:
        - name: backend
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.backend.resources | nindent 12 }}
          envFrom:
            - configMapRef:
                name: {{ include "todo.fullname" . }}-config
            - secretRef:
                name: {{ include "todo.fullname" . }}-secrets
```

### kubectl-ai Integration

```bash
# Example kubectl-ai commands for the Todo app

# Check pod status
kubectl-ai "show me all todo pods and their status"
# Generates: kubectl get pods -l app.kubernetes.io/name=todo

# Debug failing pods
kubectl-ai "why is the backend pod crashing?"
# Analyzes: kubectl describe pod, kubectl logs

# Scale deployment
kubectl-ai "scale the backend to handle more traffic"
# Suggests: kubectl scale deployment/todo-backend --replicas=4

# Resource usage
kubectl-ai "show resource usage for all todo components"
# Generates: kubectl top pods -l app.kubernetes.io/name=todo

# Network debugging
kubectl-ai "is the frontend able to reach the backend?"
# Tests connectivity, checks services and endpoints
```

---

## Phase V: Cloud Kubernetes

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        Managed Kubernetes (AKS/GKE/OKE)                       │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                    Cloud Load Balancer / Ingress                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                     │                                         │
│    ┌────────────────────────────────┼────────────────────────────────────┐   │
│    │                                │                                    │   │
│    ▼                                ▼                                    ▼   │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐       │
│  │    Frontend      │    │     Backend      │    │   AI Service     │       │
│  │    + Dapr        │    │     + Dapr       │    │    + Dapr        │       │
│  │  ┌────────────┐  │    │  ┌────────────┐  │    │  ┌────────────┐  │       │
│  │  │  Next.js   │  │    │  │  FastAPI   │  │    │  │   Agent    │  │       │
│  │  └────────────┘  │    │  └────────────┘  │    │  └────────────┘  │       │
│  │  ┌────────────┐  │    │  ┌────────────┐  │    │  ┌────────────┐  │       │
│  │  │Dapr Sidecar│  │    │  │Dapr Sidecar│  │    │  │Dapr Sidecar│  │       │
│  │  └────────────┘  │    │  └────────────┘  │    │  └────────────┘  │       │
│  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘       │
│           │                       │                       │                  │
│           └───────────────────────┼───────────────────────┘                  │
│                                   │                                          │
│  ┌────────────────────────────────▼───────────────────────────────────────┐  │
│  │                         Dapr Control Plane                              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │  │
│  │  │   Pub/Sub    │  │ State Store  │  │   Secrets    │                  │  │
│  │  │   (Kafka)    │  │   (Redis)    │  │  (Azure KV)  │                  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                  │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                   │                                          │
│  ┌────────────────────────────────▼───────────────────────────────────────┐  │
│  │                      Kafka (Redpanda/Confluent)                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │  │
│  │  │  Topics: task-events, task-created, task-updated, task-deleted  │   │  │
│  │  └─────────────────────────────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                       Observability Stack                               │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐       │  │
│  │  │ Prometheus │  │  Grafana   │  │   Jaeger   │  │    Loki    │       │  │
│  │  │  (Metrics) │  │ (Dashboards│  │  (Traces)  │  │   (Logs)   │       │  │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │      Neon Serverless DB        │
                    │        (External)              │
                    └────────────────────────────────┘
```

### Dapr Components

```yaml
# components/pubsub-kafka.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-pubsub
  namespace: todo
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka-broker:9092"
    - name: consumerGroup
      value: "todo-consumer"
    - name: authType
      value: "none"

---
# components/statestore-redis.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-statestore
  namespace: todo
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis-master:6379"
    - name: redisPassword
      secretKeyRef:
        name: redis-secret
        key: password

---
# components/secrets-azure.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: azure-keyvault
  namespace: todo
spec:
  type: secretstores.azure.keyvault
  version: v1
  metadata:
    - name: vaultName
      value: "todo-keyvault"
    - name: azureTenantId
      value: ""
    - name: azureClientId
      value: ""
```

### Event-Driven Task Service

```python
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem
import json
from datetime import datetime

class EventDrivenTaskService:
    def __init__(self):
        self.dapr = DaprClient()
        self.pubsub_name = "task-pubsub"
        self.store_name = "task-statestore"

    async def create_task(self, user_id: str, task_data: dict) -> Task:
        """Create task and publish event."""
        # Create task in database
        task = await self.db_service.create(user_id, task_data)

        # Publish event via Dapr
        event = {
            "type": "TaskCreated",
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "taskId": str(task.id),
                "userId": user_id,
                "title": task.title,
                "priority": task.priority
            },
            "metadata": {
                "correlationId": get_correlation_id(),
                "source": "todo-backend"
            }
        }

        self.dapr.publish_event(
            pubsub_name=self.pubsub_name,
            topic_name="task-created",
            data=json.dumps(event)
        )

        # Cache in state store
        self.dapr.save_state(
            store_name=self.store_name,
            key=f"task:{task.id}",
            value=json.dumps(task.model_dump())
        )

        return task

    async def get_task_cached(self, task_id: str) -> Optional[Task]:
        """Get task from cache or database."""
        # Try cache first
        state = self.dapr.get_state(
            store_name=self.store_name,
            key=f"task:{task_id}"
        )

        if state.data:
            return Task(**json.loads(state.data))

        # Fallback to database
        task = await self.db_service.get(task_id)
        if task:
            # Update cache
            self.dapr.save_state(
                store_name=self.store_name,
                key=f"task:{task_id}",
                value=json.dumps(task.model_dump())
            )

        return task
```

### Event Subscription Handler

```python
from fastapi import APIRouter, Request
from cloudevents.http import from_http

router = APIRouter()

@router.post("/events/task-created")
async def handle_task_created(request: Request):
    """Handle TaskCreated events for real-time sync."""
    event = from_http(request.headers, await request.body())
    data = event.data

    # Broadcast to connected WebSocket clients
    await websocket_manager.broadcast(
        user_id=data["userId"],
        event_type="task_created",
        payload=data
    )

    return {"status": "ok"}

@router.post("/events/task-updated")
async def handle_task_updated(request: Request):
    """Handle TaskUpdated events."""
    event = from_http(request.headers, await request.body())
    data = event.data

    # Invalidate cache
    await cache.delete(f"task:{data['taskId']}")

    # Broadcast to clients
    await websocket_manager.broadcast(
        user_id=data["userId"],
        event_type="task_updated",
        payload=data
    )

    return {"status": "ok"}
```

### Observability Configuration

```yaml
# Prometheus ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: todo-backend
  namespace: todo
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: todo
      app.kubernetes.io/component: backend
  endpoints:
    - port: http
      path: /metrics
      interval: 15s

---
# Grafana Dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  todo-dashboard.json: |
    {
      "dashboard": {
        "title": "Todo App Dashboard",
        "panels": [
          {
            "title": "Request Rate",
            "type": "stat",
            "targets": [{
              "expr": "rate(http_requests_total{app='todo-backend'}[5m])"
            }]
          },
          {
            "title": "Error Rate",
            "type": "gauge",
            "targets": [{
              "expr": "rate(http_requests_total{app='todo-backend',status=~'5..'}[5m])"
            }]
          },
          {
            "title": "Latency P95",
            "type": "stat",
            "targets": [{
              "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{app='todo-backend'}[5m]))"
            }]
          }
        ]
      }
    }
```

### Jaeger Tracing Integration

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger-agent",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Manual span example
tracer = trace.get_tracer(__name__)

async def create_task(user_id: str, task_data: dict):
    with tracer.start_as_current_span("create_task") as span:
        span.set_attribute("user.id", user_id)
        span.set_attribute("task.title", task_data["title"])

        # Create task
        task = await task_service.create(user_id, task_data)

        span.set_attribute("task.id", str(task.id))
        span.add_event("task_created")

        return task
```

---

## Cross-Phase Considerations

### Database Migration Strategy

```python
# alembic/versions/001_initial.py
"""Initial schema for Phase II"""

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(255)),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )

    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('user_id', postgresql.UUID(), sa.ForeignKey('users.id')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('status', sa.String(20)),
        sa.Column('priority', sa.String(10)),
        sa.Column('due_date', sa.Date),
        sa.Column('tags', postgresql.ARRAY(sa.String)),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
    )

# alembic/versions/002_add_conversations.py
"""Add conversations for Phase III"""

def upgrade():
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('user_id', postgresql.UUID(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('conversation_id', postgresql.UUID(),
                  sa.ForeignKey('conversations.id')),
        sa.Column('role', sa.String(20)),
        sa.Column('content', sa.Text),
        sa.Column('tool_calls', postgresql.JSONB),
        sa.Column('timestamp', sa.DateTime(timezone=True)),
    )

# alembic/versions/003_add_events.py
"""Add event sourcing for Phase V"""

def upgrade():
    op.create_table(
        'task_events',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('task_id', postgresql.UUID()),
        sa.Column('event_type', sa.String(50)),
        sa.Column('event_data', postgresql.JSONB),
        sa.Column('timestamp', sa.DateTime(timezone=True)),
        sa.Column('correlation_id', sa.String(100)),
    )

    op.create_index('idx_task_events_task_id', 'task_events', ['task_id'])
    op.create_index('idx_task_events_timestamp', 'task_events', ['timestamp'])
```

### Environment Configuration

```yaml
# config/development.yaml
environment: development
log_level: DEBUG
database:
  url: ${DATABASE_URL}
  pool_size: 5
auth:
  jwt_secret: ${JWT_SECRET}
  access_token_expire: 15  # minutes
  refresh_token_expire: 10080  # 7 days
openai:
  api_key: ${OPENAI_API_KEY}
  model: gpt-4o

# config/production.yaml
environment: production
log_level: INFO
database:
  url: ${DATABASE_URL}
  pool_size: 20
auth:
  jwt_secret: ${JWT_SECRET}
  access_token_expire: 15
  refresh_token_expire: 10080
openai:
  api_key: ${OPENAI_API_KEY}
  model: gpt-4o
kafka:
  brokers: ${KAFKA_BROKERS}
dapr:
  pubsub_name: task-pubsub
  state_store: task-statestore
observability:
  jaeger_endpoint: ${JAEGER_ENDPOINT}
  prometheus_port: 9090
```

---

## Summary

| Phase | Key Deliverables |
|-------|------------------|
| **I** | `todo.py`, in-memory storage, CLI commands |
| **II** | FastAPI backend, Next.js frontend, Neon DB, Better Auth |
| **III** | OpenAI Agent, MCP Server, Chat interface |
| **IV** | Dockerfiles, Helm charts, Minikube deployment |
| **V** | Dapr components, Kafka topics, Observability stack |

---

**Document Version**: 1.0.0
**Last Updated**: 2025-01-17
**Status**: Ready for Implementation
