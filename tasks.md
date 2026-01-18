# Todo App - Task Breakdown

## Task Organization

This document breaks down the implementation into actionable tasks organized by phase. Each task includes:
- **Task ID**: Unique identifier (T-XXX)
- **Description**: Clear task objective
- **Dependencies**: Prerequisites (which tasks must be complete first)
- **Acceptance Criteria**: How to verify task completion
- **Files to Modify**: Specific files that will be created or changed

---

## Phase I: Console Application

### T-101: Initialize Python Project
**Description**: Create Python project with pyproject.toml configuration

**Dependencies**: None

**Files to Create**:
- `todo-console/pyproject.toml`
- `todo-console/.gitignore`
- `todo-console/README.md`

**Steps**:
1. Create `todo-console` directory
2. Initialize with `uv init` or create `pyproject.toml` manually
3. Configure Python 3.13+
4. Add development dependencies (pytest, ruff)
5. Create `.gitignore` for Python

**Acceptance Criteria**:
```gherkin
Given the project is initialized
When I run `uv sync` or `pip install -e .`
Then dependencies are installed
And the project is ready for development
```

---

### T-102: Create Task Data Model
**Description**: Implement Task dataclass with all required fields

**Dependencies**: T-101

**Files to Create**:
- `todo-console/models.py`

**Reference Spec Sections**:
- specify.md → Phase I → Data Model

**Steps**:
1. Create `models.py`
2. Define `Task` dataclass with fields:
   - `id: int`
   - `title: str`
   - `description: Optional[str]`
   - `status: Literal["pending", "done"]`
   - `created_at: datetime`
   - `completed_at: Optional[datetime]`
3. Implement `mark_done()` method
4. Implement `mark_pending()` method
5. Add type hints and docstrings

**Acceptance Criteria**:
```gherkin
Given a Task is created
When I call task.mark_done()
Then status changes to "done"
And completed_at is set
When I call task.mark_pending()
Then status changes to "pending"
And completed_at is None
```

---

### T-103: Implement In-Memory Storage
**Description**: Create TaskStorage class for CRUD operations

**Dependencies**: T-102

**Files to Create**:
- `todo-console/storage.py`

**Reference Spec Sections**:
- plan.md → Phase I → Storage Layer

**Steps**:
1. Create `TaskStorage` class
2. Implement `create(title, description)` method
3. Implement `get(task_id)` method
4. Implement `list(status)` method with filtering
5. Implement `update(task_id, **kwargs)` method
6. Implement `delete(task_id)` method
7. Manage `_next_id` for sequential IDs

**Acceptance Criteria**:
```gherkin
Given an empty TaskStorage
When I create a task
Then it has ID 1
When I create another task
Then it has ID 2
When I list all tasks
Then both tasks are returned
When I delete a task
Then it's no longer in the list
```

---

### T-104: Implement Output Formatter
**Description**: Create table formatter for task display

**Dependencies**: T-102

**Files to Create**:
- `todo-console/formatter.py`

**Steps**:
1. Create `format_task_table(tasks)` function
2. Format columns: ID, Title, Status, Created
3. Handle empty task list
4. Truncate long titles (max 30 chars)
5. Format dates as YYYY-MM-DD

**Acceptance Criteria**:
```gherkin
Given a list of tasks
When formatted as a table
Then output shows headers
And each task on its own row
And columns are aligned
```

---

### T-105: Implement Command Handler
**Description**: Create CommandHandler class for all CLI commands

**Dependencies**: T-103, T-104

**Files to Create**:
- `todo-console/commands.py`

**Reference Spec Sections**:
- specify.md → Phase I → Commands Reference

**Steps**:
1. Create `CommandHandler` class
2. Implement `add(title, desc)` command
3. Implement `list(status)` command
4. Implement `done(task_id)` command
5. Implement `undo(task_id)` command
6. Implement `delete(task_id)` command
7. Implement `edit(task_id, title, desc)` command
8. Return user-friendly messages for all operations

**Acceptance Criteria**:
```gherkin
Given a CommandHandler instance
When I call handler.add("Test task")
Then a task is created
And I get a confirmation message
When I call handler.list()
Then I get a formatted table
```

---

### T-106: Create CLI Interface
**Description**: Implement interactive CLI with command parsing

**Dependencies**: T-105

**Files to Create**:
- `todo-console/todo.py`

**Steps**:
1. Create main entry point
2. Set up argparse with subcommands
3. Create interactive REPL loop
4. Display welcome message
5. Show `Todo > ` prompt
6. Parse and execute commands
7. Handle `exit` command
8. Handle `help` command
9. Handle invalid commands gracefully

**Acceptance Criteria**:
```gherkin
Given the app is started
When I type "add Buy groceries"
Then a task is created
And I see confirmation
When I type "help"
Then I see available commands
When I type "exit"
Then the app exits cleanly
```

---

### T-107: Add Error Handling
**Description**: Implement comprehensive error handling

**Dependencies**: T-106

**Files to Modify**:
- `todo-console/commands.py`
- `todo-console/todo.py`

**Steps**:
1. Handle invalid task IDs
2. Handle empty input
3. Handle invalid commands
4. Provide helpful error messages
5. Don't crash on exceptions

**Acceptance Criteria**:
```gherkin
Given an invalid task ID
When I try to mark it done
Then I get "Task not found" message
And the app continues running
```

---

### T-108: Write Phase I Tests
**Description**: Create comprehensive test suite

**Dependencies**: T-107

**Files to Create**:
- `todo-console/tests/__init__.py`
- `todo-console/tests/test_models.py`
- `todo-console/tests/test_storage.py`
- `todo-console/tests/test_commands.py`

**Steps**:
1. Test Task model creation and methods
2. Test TaskStorage CRUD operations
3. Test CommandHandler responses
4. Test edge cases (empty lists, invalid IDs)
5. Achieve 100% coverage

**Acceptance Criteria**:
```gherkin
Given the test suite
When I run pytest
Then all tests pass
And coverage is 100%
```

---

## Phase II: Web Application

### Backend Tasks

### T-201: Initialize FastAPI Backend
**Description**: Create FastAPI project structure

**Dependencies**: T-108 (Phase I complete)

**Files to Create**:
- `todo-web/backend/app/__init__.py`
- `todo-web/backend/app/main.py`
- `todo-web/backend/app/config.py`
- `todo-web/backend/pyproject.toml`
- `todo-web/backend/Dockerfile`

**Steps**:
1. Create backend directory structure
2. Initialize FastAPI app
3. Configure CORS middleware
4. Add health check endpoint (`/health`)
5. Add readiness endpoint (`/ready`)
6. Configure environment variables
7. Create Dockerfile

**Acceptance Criteria**:
```gherkin
Given the backend is running
When I call GET /health
Then I get 200 OK
And response contains {"status": "healthy"}
```

---

### T-202: Configure Database Connection
**Description**: Set up SQLModel with Neon PostgreSQL

**Dependencies**: T-201

**Files to Create**:
- `todo-web/backend/app/db/__init__.py`
- `todo-web/backend/app/db/session.py`

**Steps**:
1. Install sqlmodel and asyncpg
2. Create async engine configuration
3. Create session dependency
4. Configure connection pooling
5. Add database URL from environment

**Acceptance Criteria**:
```gherkin
Given valid DATABASE_URL
When the app starts
Then connection to Neon is established
And queries execute successfully
```

---

### T-203: Create User Model
**Description**: Implement User SQLModel

**Dependencies**: T-202

**Files to Create**:
- `todo-web/backend/app/models/__init__.py`
- `todo-web/backend/app/models/user.py`

**Steps**:
1. Create User SQLModel class
2. Define fields: id, email, name, created_at
3. Add email uniqueness constraint
4. Add timestamps

**Acceptance Criteria**:
```gherkin
Given the User model
When I create a user
Then it has a UUID id
And email is unique
And created_at is set
```

---

### T-204: Create Task Model
**Description**: Implement Task SQLModel with all fields

**Dependencies**: T-203

**Files to Create**:
- `todo-web/backend/app/models/task.py`

**Reference Spec Sections**:
- specify.md → Phase II → Data Model
- plan.md → Phase II → SQLModel Task Model

**Steps**:
1. Create TaskStatus enum
2. Create TaskPriority enum
3. Create TaskBase model
4. Create Task table model
5. Create TaskCreate model
6. Create TaskUpdate model
7. Add foreign key to users

**Acceptance Criteria**:
```gherkin
Given the Task model
When I create a task
Then it has all required fields
And foreign key to user_id works
And enums validate correctly
```

---

### T-205: Implement Task Service
**Description**: Create business logic layer for tasks

**Dependencies**: T-204

**Files to Create**:
- `todo-web/backend/app/services/__init__.py`
- `todo-web/backend/app/services/tasks.py`

**Reference Spec Sections**:
- plan.md → Phase II → Task Service

**Steps**:
1. Create TaskService class
2. Implement `create(user_id, task_in)` method
3. Implement `get(task_id, user_id)` method
4. Implement `list(user_id, filters)` method
5. Implement `update(task_id, user_id, task_in)` method
6. Implement `delete(task_id, user_id)` method
7. Add user authorization checks

**Acceptance Criteria**:
```gherkin
Given a user
When they create a task
Then the task belongs to that user
When another user tries to access it
Then they get 404
```

---

### T-206: Implement Task Router
**Description**: Create REST API endpoints for tasks

**Dependencies**: T-205

**Files to Create**:
- `todo-web/backend/app/routers/__init__.py`
- `todo-web/backend/app/routers/tasks.py`

**Reference Spec Sections**:
- specify.md → Phase II → API Endpoints

**Steps**:
1. Create APIRouter for tasks
2. Implement `GET /api/tasks` with filters
3. Implement `POST /api/tasks`
4. Implement `GET /api/tasks/{id}`
5. Implement `PATCH /api/tasks/{id}`
6. Implement `DELETE /api/tasks/{id}`
7. Add authentication dependency
8. Add pagination

**Acceptance Criteria**:
```gherkin
Given an authenticated user
When they POST to /api/tasks
Then a task is created
And 201 is returned
When they GET /api/tasks
Then their tasks are listed
```

---

### T-207: Integrate Better Auth
**Description**: Set up authentication with Better Auth

**Dependencies**: T-206

**Files to Create**:
- `todo-web/backend/app/routers/auth.py`
- `todo-web/backend/app/middleware/auth.py`

**Reference Spec Sections**:
- constitution.md → Phase II constraints
- specify.md → Phase II → FR-2.1 User Authentication

**Steps**:
1. Install Better Auth Python client
2. Create auth router
3. Implement `POST /api/auth/register`
4. Implement `POST /api/auth/login`
5. Implement `POST /api/auth/refresh`
6. Implement `POST /api/auth/logout`
7. Create auth middleware for protected routes
8. Configure JWT validation

**Acceptance Criteria**:
```gherkin
Given valid credentials
When I POST to /api/auth/login
Then I get access and refresh tokens
When I use the access token
Then protected routes work
```

---

### T-208: Add Database Migrations
**Description**: Set up Alembic for migrations

**Dependencies**: T-207

**Files to Create**:
- `todo-web/backend/alembic.ini`
- `todo-web/backend/app/db/migrations/env.py`
- `todo-web/backend/app/db/migrations/versions/001_initial.py`

**Steps**:
1. Initialize Alembic
2. Configure for async
3. Create initial migration (users, tasks tables)
4. Add indexes
5. Test migration up/down

**Acceptance Criteria**:
```gherkin
Given an empty database
When I run alembic upgrade head
Then all tables are created
When I run alembic downgrade base
Then all tables are dropped
```

---

### T-209: Write Backend Tests
**Description**: Create comprehensive backend test suite

**Dependencies**: T-208

**Files to Create**:
- `todo-web/backend/tests/__init__.py`
- `todo-web/backend/tests/conftest.py`
- `todo-web/backend/tests/test_tasks.py`
- `todo-web/backend/tests/test_auth.py`

**Steps**:
1. Set up pytest-asyncio
2. Create test database fixtures
3. Test all task endpoints
4. Test all auth endpoints
5. Test authorization
6. Achieve 80%+ coverage

**Acceptance Criteria**:
```gherkin
Given the test suite
When I run pytest
Then all tests pass
And coverage is >= 80%
```

---

### Frontend Tasks

### T-210: Initialize Next.js Frontend
**Description**: Create Next.js 15 project with App Router

**Dependencies**: T-209

**Files to Create**:
- `todo-web/frontend/package.json`
- `todo-web/frontend/next.config.js`
- `todo-web/frontend/tailwind.config.js`
- `todo-web/frontend/src/app/layout.tsx`
- `todo-web/frontend/src/app/page.tsx`
- `todo-web/frontend/Dockerfile`

**Steps**:
1. Initialize with `npx create-next-app@latest`
2. Configure TypeScript strict mode
3. Set up Tailwind CSS
4. Configure App Router
5. Create root layout
6. Create Dockerfile

**Acceptance Criteria**:
```gherkin
Given the frontend project
When I run npm run dev
Then the app starts on port 3000
And Tailwind styles work
```

---

### T-211: Set Up API Client
**Description**: Create typed API client for backend

**Dependencies**: T-210

**Files to Create**:
- `todo-web/frontend/src/lib/api.ts`
- `todo-web/frontend/src/types/index.ts`

**Steps**:
1. Define TypeScript interfaces
2. Create API client class
3. Implement auth methods
4. Implement task CRUD methods
5. Handle errors consistently
6. Add token refresh logic

**Acceptance Criteria**:
```gherkin
Given the API client
When I call api.getTasks()
Then tasks are returned with correct types
When the token expires
Then it's refreshed automatically
```

---

### T-212: Create Auth Pages
**Description**: Implement login and register pages

**Dependencies**: T-211

**Files to Create**:
- `todo-web/frontend/src/app/(auth)/login/page.tsx`
- `todo-web/frontend/src/app/(auth)/register/page.tsx`
- `todo-web/frontend/src/components/auth/login-form.tsx`
- `todo-web/frontend/src/components/auth/register-form.tsx`

**Steps**:
1. Create login page with form
2. Create register page with form
3. Implement form validation with Zod
4. Handle auth state
5. Redirect after login
6. Style with Tailwind

**Acceptance Criteria**:
```gherkin
Given the login page
When I enter valid credentials
Then I'm redirected to dashboard
When I enter invalid credentials
Then I see error message
```

---

### T-213: Create Dashboard Layout
**Description**: Implement authenticated dashboard layout

**Dependencies**: T-212

**Files to Create**:
- `todo-web/frontend/src/app/(dashboard)/layout.tsx`
- `todo-web/frontend/src/components/layout/sidebar.tsx`
- `todo-web/frontend/src/components/layout/header.tsx`

**Steps**:
1. Create dashboard layout
2. Implement sidebar navigation
3. Implement header with user menu
4. Add logout functionality
5. Protect routes with auth check

**Acceptance Criteria**:
```gherkin
Given an authenticated user
When they access dashboard
Then sidebar and header appear
When they click logout
Then they're redirected to login
```

---

### T-214: Implement Task List
**Description**: Create task list component with TanStack Query

**Dependencies**: T-213

**Files to Create**:
- `todo-web/frontend/src/components/task/task-list.tsx`
- `todo-web/frontend/src/components/task/task-card.tsx`
- `todo-web/frontend/src/components/task/task-list-skeleton.tsx`

**Reference Spec Sections**:
- plan.md → Phase II → Task List Component

**Steps**:
1. Set up TanStack Query provider
2. Create TaskList component
3. Create TaskCard component
4. Implement loading skeleton
5. Implement empty state
6. Add optimistic updates

**Acceptance Criteria**:
```gherkin
Given tasks exist
When TaskList renders
Then all tasks display
When I toggle a task
Then UI updates immediately
And syncs with server
```

---

### T-215: Implement Task Form
**Description**: Create task creation and editing forms

**Dependencies**: T-214

**Files to Create**:
- `todo-web/frontend/src/components/task/task-form.tsx`
- `todo-web/frontend/src/components/task/task-modal.tsx`

**Steps**:
1. Create TaskForm with React Hook Form
2. Add validation with Zod
3. Implement create mode
4. Implement edit mode
5. Add date picker for due date
6. Add priority selector
7. Add tag input

**Acceptance Criteria**:
```gherkin
Given the task form
When I submit valid data
Then task is created/updated
When I submit invalid data
Then validation errors show
```

---

### T-216: Create Dashboard Views
**Description**: Implement Today, Upcoming, All Tasks views

**Dependencies**: T-215

**Files to Create**:
- `todo-web/frontend/src/app/(dashboard)/today/page.tsx`
- `todo-web/frontend/src/app/(dashboard)/upcoming/page.tsx`
- `todo-web/frontend/src/app/(dashboard)/tasks/page.tsx`

**Reference Spec Sections**:
- specify.md → Phase II → FR-2.4 Dashboard Views

**Steps**:
1. Create Today view (due today + overdue)
2. Create Upcoming view (next 7 days)
3. Create All Tasks view with filters
4. Add filter controls
5. Add sorting options

**Acceptance Criteria**:
```gherkin
Given tasks with various due dates
When I view Today
Then only today's and overdue tasks show
When I view Upcoming
Then next 7 days tasks show
```

---

### T-217: Add Keyboard Shortcuts
**Description**: Implement keyboard navigation

**Dependencies**: T-216

**Files to Modify**:
- `todo-web/frontend/src/app/(dashboard)/layout.tsx`
- `todo-web/frontend/src/components/task/task-list.tsx`

**Steps**:
1. Add "n" shortcut for new task
2. Add "j/k" for list navigation
3. Add "Enter" to toggle task
4. Add "/" for search focus
5. Show keyboard shortcuts help

**Acceptance Criteria**:
```gherkin
Given the dashboard
When I press "n"
Then new task modal opens
When I press "j"
Then next task is selected
```

---

### T-218: Write Frontend Tests
**Description**: Create frontend test suite

**Dependencies**: T-217

**Files to Create**:
- `todo-web/frontend/src/__tests__/components/task-list.test.tsx`
- `todo-web/frontend/src/__tests__/components/task-form.test.tsx`

**Steps**:
1. Set up Vitest and React Testing Library
2. Mock API client
3. Test TaskList component
4. Test TaskForm component
5. Test auth flows

**Acceptance Criteria**:
```gherkin
Given the test suite
When I run npm test
Then all tests pass
```

---

### T-219: Create Docker Compose Setup
**Description**: Docker Compose for local development

**Dependencies**: T-218

**Files to Create**:
- `todo-web/docker-compose.yml`
- `todo-web/docker-compose.dev.yml`

**Steps**:
1. Create docker-compose.yml
2. Configure backend service
3. Configure frontend service
4. Add PostgreSQL for local dev
5. Configure networking
6. Add hot reload for development

**Acceptance Criteria**:
```gherkin
Given docker-compose.yml
When I run docker-compose up
Then all services start
And the app is accessible
```

---

## Phase III: AI Chatbot

### T-301: Create AI Service Structure
**Description**: Initialize AI service with OpenAI Agents SDK

**Dependencies**: T-219 (Phase II complete)

**Files to Create**:
- `todo-web/ai-service/app/__init__.py`
- `todo-web/ai-service/app/main.py`
- `todo-web/ai-service/pyproject.toml`
- `todo-web/ai-service/Dockerfile`

**Steps**:
1. Create ai-service directory
2. Install openai-agents-sdk
3. Create FastAPI app
4. Configure OpenAI API key
5. Create Dockerfile

**Acceptance Criteria**:
```gherkin
Given the AI service
When I start it
Then it connects to OpenAI
And health check passes
```

---

### T-302: Implement MCP Server
**Description**: Create MCP server with todo tools

**Dependencies**: T-301

**Files to Create**:
- `todo-web/ai-service/app/mcp/__init__.py`
- `todo-web/ai-service/app/mcp/server.py`
- `todo-web/ai-service/app/mcp/tools.py`

**Reference Spec Sections**:
- specify.md → Phase III → FR-3.4 MCP Tool Integration
- plan.md → Phase III → MCP Server Implementation

**Steps**:
1. Install mcp-sdk
2. Create MCP server
3. Implement `create_task` tool
4. Implement `list_tasks` tool
5. Implement `update_task` tool
6. Implement `delete_task` tool
7. Implement `get_task` tool
8. Add tool schemas

**Acceptance Criteria**:
```gherkin
Given the MCP server
When I call create_task
Then a task is created via API
And confirmation is returned
```

---

### T-303: Configure Agent
**Description**: Set up OpenAI Agent with MCP tools

**Dependencies**: T-302

**Files to Create**:
- `todo-web/ai-service/app/agent/__init__.py`
- `todo-web/ai-service/app/agent/config.py`
- `todo-web/ai-service/app/agent/runner.py`

**Reference Spec Sections**:
- plan.md → Phase III → Agent Configuration

**Steps**:
1. Define agent instructions
2. Configure gpt-4o model
3. Register MCP tools
4. Create agent runner
5. Configure streaming

**Acceptance Criteria**:
```gherkin
Given the agent
When I send a message
Then it uses appropriate tools
And responds helpfully
```

---

### T-304: Implement Chat Endpoint
**Description**: Create streaming chat API

**Dependencies**: T-303

**Files to Create**:
- `todo-web/ai-service/app/routers/chat.py`

**Reference Spec Sections**:
- plan.md → Phase III → Chat Endpoint

**Steps**:
1. Create chat router
2. Implement `/api/chat/message` endpoint
3. Return Server-Sent Events
4. Stream agent responses
5. Include conversation ID

**Acceptance Criteria**:
```gherkin
Given a chat message
When I POST to /api/chat/message
Then I get streaming response
And tool calls are executed
```

---

### T-305: Add Conversation Persistence
**Description**: Store conversations in database

**Dependencies**: T-304

**Files to Modify**:
- `todo-web/backend/app/models/`
- `todo-web/backend/app/db/migrations/`

**Files to Create**:
- `todo-web/backend/app/models/conversation.py`
- `todo-web/backend/app/models/message.py`

**Steps**:
1. Create Conversation model
2. Create Message model
3. Add migration
4. Implement conversation service
5. Load history on new messages

**Acceptance Criteria**:
```gherkin
Given a conversation
When I close and reopen
Then previous messages are loaded
And context is maintained
```

---

### T-306: Create Chat UI
**Description**: Implement chat interface in frontend

**Dependencies**: T-305

**Files to Create**:
- `todo-web/frontend/src/app/(dashboard)/chat/page.tsx`
- `todo-web/frontend/src/components/chat/chat-interface.tsx`
- `todo-web/frontend/src/components/chat/message-list.tsx`
- `todo-web/frontend/src/components/chat/message-input.tsx`

**Steps**:
1. Create chat page
2. Implement message list
3. Implement input field
4. Handle streaming responses
5. Show tool call indicators
6. Style chat bubbles

**Acceptance Criteria**:
```gherkin
Given the chat page
When I type a message
Then AI responds with streaming
And I can see when tools are called
```

---

### T-307: Test AI Integration
**Description**: Test agent behavior

**Dependencies**: T-306

**Files to Create**:
- `todo-web/ai-service/tests/test_agent.py`
- `todo-web/ai-service/tests/test_tools.py`

**Steps**:
1. Test tool execution
2. Test intent recognition
3. Test multi-turn conversation
4. Test error handling
5. Mock OpenAI API

**Acceptance Criteria**:
```gherkin
Given test scenarios
When I run tests
Then all pass
And edge cases are covered
```

---

## Phase IV: Local Kubernetes

### T-401: Create Dockerfiles
**Description**: Production-ready Dockerfiles for all services

**Dependencies**: T-307 (Phase III complete)

**Files to Modify**:
- `todo-web/backend/Dockerfile`
- `todo-web/frontend/Dockerfile`
- `todo-web/ai-service/Dockerfile`

**Steps**:
1. Create multi-stage Dockerfile for backend
2. Create multi-stage Dockerfile for frontend
3. Create Dockerfile for AI service
4. Optimize image sizes
5. Add health checks
6. Configure non-root users

**Acceptance Criteria**:
```gherkin
Given the Dockerfiles
When I build images
Then they are < 500MB each
And health checks work
```

---

### T-402: Create Helm Chart Structure
**Description**: Initialize Helm chart for todo app

**Dependencies**: T-401

**Files to Create**:
- `charts/todo/Chart.yaml`
- `charts/todo/values.yaml`
- `charts/todo/templates/_helpers.tpl`
- `charts/todo/templates/NOTES.txt`

**Reference Spec Sections**:
- plan.md → Phase IV → Helm Chart Structure

**Steps**:
1. Create charts directory
2. Initialize Chart.yaml
3. Create values.yaml with defaults
4. Create helper templates
5. Create NOTES.txt

**Acceptance Criteria**:
```gherkin
Given the Helm chart
When I run helm lint
Then no errors are found
```

---

### T-403: Create Backend Deployment
**Description**: Kubernetes manifests for backend

**Dependencies**: T-402

**Files to Create**:
- `charts/todo/templates/backend/deployment.yaml`
- `charts/todo/templates/backend/service.yaml`
- `charts/todo/templates/backend/hpa.yaml`

**Reference Spec Sections**:
- plan.md → Phase IV → Deployment Templates

**Steps**:
1. Create Deployment with probes
2. Create ClusterIP Service
3. Create HorizontalPodAutoscaler
4. Configure resource limits
5. Add environment variables

**Acceptance Criteria**:
```gherkin
Given the backend templates
When deployed to Minikube
Then pods are running
And service is accessible
```

---

### T-404: Create Frontend Deployment
**Description**: Kubernetes manifests for frontend

**Dependencies**: T-403

**Files to Create**:
- `charts/todo/templates/frontend/deployment.yaml`
- `charts/todo/templates/frontend/service.yaml`
- `charts/todo/templates/frontend/hpa.yaml`

**Steps**:
1. Create Deployment
2. Create Service
3. Create HPA
4. Configure Nginx for SPA routing

**Acceptance Criteria**:
```gherkin
Given the frontend templates
When deployed
Then pods are running
And client-side routing works
```

---

### T-405: Create AI Service Deployment
**Description**: Kubernetes manifests for AI service

**Dependencies**: T-404

**Files to Create**:
- `charts/todo/templates/ai-service/deployment.yaml`
- `charts/todo/templates/ai-service/service.yaml`

**Steps**:
1. Create Deployment
2. Create Service
3. Configure OpenAI API key secret
4. Set appropriate resource limits

**Acceptance Criteria**:
```gherkin
Given the AI service templates
When deployed
Then pod is running
And chat API works
```

---

### T-406: Create Ingress Configuration
**Description**: Configure ingress for routing

**Dependencies**: T-405

**Files to Create**:
- `charts/todo/templates/ingress.yaml`

**Reference Spec Sections**:
- plan.md → Phase IV → Values Configuration

**Steps**:
1. Create Ingress resource
2. Configure NGINX ingress class
3. Route `/` to frontend
4. Route `/api` to backend
5. Route `/api/chat` to AI service

**Acceptance Criteria**:
```gherkin
Given the Ingress
When I access todo.local
Then frontend loads
When I access /api/tasks
Then backend responds
```

---

### T-407: Create ConfigMaps and Secrets
**Description**: External configuration management

**Dependencies**: T-406

**Files to Create**:
- `charts/todo/templates/configmap.yaml`
- `charts/todo/templates/secrets.yaml`

**Steps**:
1. Create ConfigMap for app config
2. Create Secret template
3. Configure environment variable references
4. Add sealed secrets option

**Acceptance Criteria**:
```gherkin
Given ConfigMaps and Secrets
When pods start
Then environment variables are set
And secrets are not exposed
```

---

### T-408: Test Minikube Deployment
**Description**: End-to-end deployment test

**Dependencies**: T-407

**Files to Create**:
- `scripts/deploy-local.sh`
- `scripts/test-deployment.sh`

**Steps**:
1. Start Minikube
2. Build and load images
3. Deploy with Helm
4. Run smoke tests
5. Test all endpoints
6. Test scaling

**Acceptance Criteria**:
```gherkin
Given Minikube is running
When I run deploy-local.sh
Then app is deployed
And all tests pass
```

---

### T-409: Document kubectl-ai Usage
**Description**: Create kubectl-ai examples

**Dependencies**: T-408

**Files to Create**:
- `docs/kubectl-ai-examples.md`

**Steps**:
1. Document common queries
2. Document troubleshooting commands
3. Create example scenarios
4. Test all examples

**Acceptance Criteria**:
```gherkin
Given the documentation
When I follow examples
Then kubectl-ai works correctly
```

---

## Phase V: Cloud Kubernetes

### T-501: Set Up Kafka/Redpanda
**Description**: Deploy event streaming platform

**Dependencies**: T-409 (Phase IV complete)

**Files to Create**:
- `charts/todo/charts/redpanda/`
- `charts/todo/templates/kafka-topics.yaml`

**Steps**:
1. Add Redpanda as subchart
2. Create topics: task-events, task-created, task-updated
3. Configure retention
4. Test message publishing

**Acceptance Criteria**:
```gherkin
Given Kafka is deployed
When I publish an event
Then consumers receive it
```

---

### T-502: Install Dapr
**Description**: Deploy Dapr control plane

**Dependencies**: T-501

**Files to Create**:
- `charts/todo/templates/dapr/`
- `scripts/install-dapr.sh`

**Steps**:
1. Install Dapr CLI
2. Deploy Dapr to cluster
3. Verify sidecar injection
4. Test Dapr dashboard

**Acceptance Criteria**:
```gherkin
Given Dapr is installed
When pods start
Then sidecars are injected
```

---

### T-503: Configure Dapr Components
**Description**: Set up Dapr building blocks

**Dependencies**: T-502

**Files to Create**:
- `charts/todo/templates/dapr-components/pubsub.yaml`
- `charts/todo/templates/dapr-components/statestore.yaml`
- `charts/todo/templates/dapr-components/secrets.yaml`

**Reference Spec Sections**:
- plan.md → Phase V → Dapr Components

**Steps**:
1. Create Pub/Sub component (Kafka)
2. Create State Store component (Redis)
3. Create Secrets component
4. Test each component

**Acceptance Criteria**:
```gherkin
Given Dapr components
When I publish via Dapr
Then Kafka receives message
When I save state
Then Redis stores it
```

---

### T-504: Implement Event Publishing
**Description**: Publish task events via Dapr

**Dependencies**: T-503

**Files to Modify**:
- `todo-web/backend/app/services/tasks.py`

**Reference Spec Sections**:
- plan.md → Phase V → Event-Driven Task Service

**Steps**:
1. Add Dapr client
2. Publish TaskCreated events
3. Publish TaskUpdated events
4. Publish TaskDeleted events
5. Include correlation IDs

**Acceptance Criteria**:
```gherkin
Given a task is created
When the operation completes
Then TaskCreated event is published
And event contains task data
```

---

### T-505: Implement Event Subscriptions
**Description**: Handle events for real-time sync

**Dependencies**: T-504

**Files to Create**:
- `todo-web/backend/app/routers/events.py`
- `todo-web/frontend/src/lib/websocket.ts`

**Reference Spec Sections**:
- plan.md → Phase V → Event Subscription Handler

**Steps**:
1. Create event handler endpoints
2. Configure Dapr subscriptions
3. Implement WebSocket manager
4. Broadcast to connected clients
5. Update UI in real-time

**Acceptance Criteria**:
```gherkin
Given two clients viewing tasks
When one creates a task
Then both see the update
Without manual refresh
```

---

### T-506: Add State Caching
**Description**: Implement Dapr state store caching

**Dependencies**: T-505

**Files to Modify**:
- `todo-web/backend/app/services/tasks.py`

**Steps**:
1. Cache tasks on read
2. Invalidate on write
3. Implement cache-aside pattern
4. Configure TTL

**Acceptance Criteria**:
```gherkin
Given a task is read
When it's read again
Then cache is hit
And response is faster
```

---

### T-507: Deploy Observability Stack
**Description**: Set up Prometheus, Grafana, Jaeger, Loki

**Dependencies**: T-506

**Files to Create**:
- `charts/todo/charts/prometheus/`
- `charts/todo/charts/grafana/`
- `charts/todo/charts/jaeger/`
- `charts/todo/templates/servicemonitor.yaml`

**Steps**:
1. Deploy Prometheus
2. Deploy Grafana
3. Deploy Jaeger
4. Deploy Loki
5. Configure ServiceMonitors
6. Create dashboards

**Acceptance Criteria**:
```gherkin
Given observability stack
When I access Grafana
Then I see metrics dashboards
When I access Jaeger
Then I see distributed traces
```

---

### T-508: Instrument Applications
**Description**: Add metrics, logs, and traces

**Dependencies**: T-507

**Files to Modify**:
- `todo-web/backend/app/main.py`
- `todo-web/ai-service/app/main.py`

**Reference Spec Sections**:
- plan.md → Phase V → Jaeger Tracing Integration

**Steps**:
1. Add OpenTelemetry instrumentation
2. Configure Jaeger exporter
3. Add custom spans
4. Configure structured logging
5. Add Prometheus metrics

**Acceptance Criteria**:
```gherkin
Given instrumented apps
When requests flow through
Then traces appear in Jaeger
And metrics in Prometheus
```

---

### T-509: Create Grafana Dashboards
**Description**: Build monitoring dashboards

**Dependencies**: T-508

**Files to Create**:
- `charts/todo/templates/grafana-dashboards/`

**Reference Spec Sections**:
- plan.md → Phase V → Observability Configuration

**Steps**:
1. Create request rate panel
2. Create error rate panel
3. Create latency percentiles panel
4. Create resource usage panel
5. Configure alerts

**Acceptance Criteria**:
```gherkin
Given the dashboard
When I open Grafana
Then I see all panels
And data is real-time
```

---

### T-510: Deploy to Cloud Provider
**Description**: Deploy to managed Kubernetes (AKS/GKE/OKE)

**Dependencies**: T-509

**Files to Create**:
- `scripts/deploy-cloud.sh`
- `charts/todo/values-production.yaml`

**Steps**:
1. Create managed cluster
2. Configure kubectl context
3. Deploy all components
4. Configure cloud load balancer
5. Set up DNS
6. Enable TLS

**Acceptance Criteria**:
```gherkin
Given cloud cluster
When I access the domain
Then app loads over HTTPS
And all features work
```

---

### T-511: Load Testing
**Description**: Verify scalability requirements

**Dependencies**: T-510

**Files to Create**:
- `tests/load/k6-test.js`

**Steps**:
1. Create k6 load test
2. Test 1000 concurrent users
3. Test event throughput
4. Verify auto-scaling
5. Document results

**Acceptance Criteria**:
```gherkin
Given load test
When 1000 users hit the app
Then p95 latency < 200ms
And no errors occur
```

---

## Summary Statistics

### By Phase

| Phase | Tasks | Focus |
|-------|-------|-------|
| Phase I: Console | 8 tasks | Python CLI |
| Phase II: Web App | 19 tasks | Full-stack web |
| Phase III: AI | 7 tasks | Agent integration |
| Phase IV: Local K8s | 9 tasks | Container orchestration |
| Phase V: Cloud K8s | 11 tasks | Distributed systems |
| **TOTAL** | **54 tasks** | |

### Critical Path

```
Phase I: T-101 → T-102 → T-103 → T-105 → T-106 → T-108

Phase II: T-201 → T-202 → T-204 → T-205 → T-206 → T-207 → T-209
          T-210 → T-211 → T-214 → T-215 → T-216 → T-219

Phase III: T-301 → T-302 → T-303 → T-304 → T-306 → T-307

Phase IV: T-401 → T-402 → T-403 → T-406 → T-408

Phase V: T-501 → T-502 → T-503 → T-504 → T-505 → T-508 → T-510
```

### Task Dependencies Graph

```
PHASE I                    PHASE II                    PHASE III
┌─────┐                    ┌─────┐                     ┌─────┐
│T-101│──┬────────────────►│T-201│──┬─────────────────►│T-301│
└─────┘  │                 └─────┘  │                  └─────┘
         ▼                    │     │                     │
      ┌─────┐                 ▼     │                     ▼
      │T-102│              ┌─────┐  │                  ┌─────┐
      └─────┘──┐           │T-202│  │                  │T-302│
               │           └─────┘  │                  └─────┘
               ▼              │     │                     │
            ┌─────┐           ▼     │                     ▼
            │T-103│        ┌─────┐  │                  ┌─────┐
            └─────┘──┬─────│T-204│  │                  │T-303│
                     │     └─────┘  │                  └─────┘
                     │        │     │                     │
      ┌─────┐        │        ▼     │                     ▼
      │T-104│────────┤     ┌─────┐  │                  ┌─────┐
      └─────┘        │     │T-205│  │                  │T-304│
                     ▼     └─────┘  │                  └─────┘
                  ┌─────┐     │     │                     │
                  │T-105│     ▼     │                     ▼
                  └─────┘  ┌─────┐  │                  ┌─────┐
                     │     │T-206│  │                  │T-306│
                     ▼     └─────┘  │                  └─────┘
                  ┌─────┐     │     │                     │
                  │T-106│     ▼     │                     ▼
                  └─────┘  ┌─────┐  │                  ┌─────┐
                     │     │T-207│◄─┘                  │T-307│
                     ▼     └─────┘                     └─────┘
                  ┌─────┐     │
                  │T-108│     ▼
                  └─────┘  ┌─────┐
                           │T-219│
                           └─────┘


PHASE IV                   PHASE V
┌─────┐                    ┌─────┐
│T-401│──┬────────────────►│T-501│
└─────┘  │                 └─────┘
         ▼                    │
      ┌─────┐                 ▼
      │T-402│              ┌─────┐
      └─────┘──┐           │T-502│
               │           └─────┘
               ▼              │
            ┌─────┐           ▼
            │T-403│        ┌─────┐
            └─────┘──┐     │T-503│
                     │     └─────┘
               ┌─────┤        │
               │     │        ▼
               ▼     │     ┌─────┐
            ┌─────┐  │     │T-504│
            │T-404│  │     └─────┘
            └─────┘  │        │
               │     │        ▼
               ▼     │     ┌─────┐
            ┌─────┐  │     │T-505│
            │T-405│  │     └─────┘
            └─────┘  │        │
               │     │        ▼
               └─────┼─────┌─────┐
                     │     │T-508│
                     ▼     └─────┘
                  ┌─────┐     │
                  │T-406│     ▼
                  └─────┘  ┌─────┐
                     │     │T-510│
                     ▼     └─────┘
                  ┌─────┐
                  │T-408│
                  └─────┘
```

---

## Next Steps

1. **Start with Phase I** - Console app provides foundation
2. **Complete each phase** before moving to next
3. **Run tests** before marking tasks complete
4. **Update specs** if changes are needed
5. **Document deviations** as per constitution

---

**Document Version**: 1.0.0
**Last Updated**: 2025-01-17
**Status**: Ready for Implementation
**Total Tasks**: 54
