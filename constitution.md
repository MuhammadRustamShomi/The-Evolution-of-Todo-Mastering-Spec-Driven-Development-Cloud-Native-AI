# Todo App Hackathon - Project Constitution

## Purpose

This constitution defines the non-negotiable principles, technical standards, and architectural constraints that govern all development decisions across all five phases of the Todo App evolution. Every agent, developer, and contributor must adhere to these principles.

---

## Core Values

### 1. Spec-Driven Development
- **No code without specification**: Every feature must have a corresponding entry in `speckit.specify`
- **No architecture without plan**: System changes require updates to `speckit.plan`
- **No implementation without tasks**: Code must map to specific task IDs in `speckit.tasks`
- **Iterative refinement**: Specs evolve through feedback; code follows specs, not intuition

### 2. AI-Native Development
- **Claude Code First**: Use Claude Code as the primary development tool
- **Prompt engineering over manual coding**: Refine specifications until Claude generates correct output
- **Reusable intelligence**: Build and leverage agent skills and subagents
- **Documentation as code**: All architectural decisions must be documented in markdown

### 3. Progressive Evolution
- **Each phase builds on previous**: No skipping phases; maintain backward compatibility
- **Incremental complexity**: Start simple (console) → end complex (distributed cloud)
- **Learning through building**: Each phase teaches new concepts and technologies

---

## Code Quality Standards

### General Principles
1. **Clarity over cleverness**: Code should be self-documenting and easy to understand
2. **Consistency over individual style**: Follow established patterns across the codebase
3. **Composition over inheritance**: Favor functional composition and dependency injection
4. **Fail fast and loud**: Use explicit error handling; never silently fail
5. **Immutability by default**: Prefer immutable data structures; mutate only when necessary

### Python (Backend) Standards

#### Code Organization
```python
# Required structure for Python modules
"""
Module docstring explaining purpose and usage.
"""

from typing import List, Optional, Dict
import standard_library_imports
import third_party_imports
import local_imports

# Constants
MAX_TASKS_PER_USER = 1000
DEFAULT_PAGE_SIZE = 20

# Type definitions
TaskID = int
UserID = str

# Functions and classes with type hints
def create_task(user_id: UserID, title: str, description: Optional[str] = None) -> TaskID:
    """
    Create a new task for a user.
    
    Args:
        user_id: Unique identifier for the user
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)
        
    Returns:
        The ID of the newly created task
        
    Raises:
        ValueError: If title is empty or too long
        UserNotFoundError: If user_id doesn't exist
    """
    pass
```

#### Code Style
- **Use type hints everywhere**: Every function parameter and return value
- **Docstrings required**: All public functions, classes, and modules
- **Async by default**: Use `async/await` for I/O operations
- **Context managers**: Use `with` statements for resource management
- **F-strings only**: No `.format()` or `%` formatting
- **Max line length**: 100 characters
- **Imports**: Group by standard/third-party/local, alphabetize within groups

#### Error Handling
```python
# Good: Explicit, typed, informative
from fastapi import HTTPException

async def get_task(task_id: int) -> Task:
    task = await db.fetch_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    return task

# Bad: Generic, vague, swallowed
try:
    task = get_task(task_id)
except:
    pass  # NEVER DO THIS
```

#### Database Operations
- **Use SQLModel**: Pydantic models + SQLAlchemy = type-safe ORM
- **Connection pooling**: Always use connection pools, never raw connections
- **Async sessions**: Use `AsyncSession` for all database operations
- **Transactions**: Group related operations in transactions
- **Migrations**: All schema changes via Alembic migrations

### TypeScript/JavaScript (Frontend) Standards

#### Code Organization
```typescript
// Required structure for TypeScript modules
/**
 * Module description
 * @module components/TaskList
 */

import { useState, useEffect } from 'react'
import type { Task, TaskStatus } from '@/types'
import { api } from '@/lib/api'

interface TaskListProps {
  userId: string
  status?: TaskStatus
}

/**
 * Displays a list of tasks with filtering and actions
 */
export function TaskList({ userId, status = 'all' }: TaskListProps) {
  // Implementation
}
```

#### Code Style
- **TypeScript strict mode**: Enable all strict checks
- **Server components by default**: Use Client Components only when needed
- **Named exports**: Prefer named exports over default exports
- **Functional components**: No class components
- **Hooks for state**: Use hooks; avoid prop drilling
- **Tailwind for styling**: No inline styles or CSS-in-JS
- **Max line length**: 100 characters

#### React Patterns
```typescript
// Good: Server Component (default)
export async function TaskList({ userId }: { userId: string }) {
  const tasks = await api.getTasks(userId)
  return <div>{tasks.map(task => <TaskCard key={task.id} task={task} />)}</div>
}

// Good: Client Component (when needed)
'use client'
export function TaskForm() {
  const [title, setTitle] = useState('')
  // Interactive logic here
}

// Bad: Unnecessary Client Component
'use client'  // WHY? This could be a Server Component
export function StaticHeader() {
  return <h1>My Tasks</h1>
}
```

#### Error Handling
```typescript
// Good: Granular error boundaries
import { ErrorBoundary } from '@/components/ErrorBoundary'

export function TaskPage() {
  return (
    <ErrorBoundary fallback={<TaskListError />}>
      <TaskList />
    </ErrorBoundary>
  )
}

// Good: API error handling
try {
  await api.createTask(data)
} catch (error) {
  if (error instanceof ApiError) {
    toast.error(error.message)
  } else {
    toast.error('An unexpected error occurred')
    logError(error)
  }
}
```

---

## Testing Standards

### Coverage Requirements
- **Unit tests**: Minimum 80% coverage for business logic
- **Integration tests**: All API endpoints must have integration tests
- **E2E tests**: Critical user journeys must have end-to-end tests
- **No deployment without tests**: CI must pass all tests before merge

### Python Testing (pytest)
```python
# tests/test_tasks.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_task():
    """Test task creation with valid data"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/tasks",
            json={"title": "Test task", "description": "Test description"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test task"
        assert "id" in data

@pytest.mark.asyncio
async def test_create_task_invalid_title():
    """Test task creation rejects empty title"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/tasks",
            json={"title": "", "description": "Test"}
        )
        assert response.status_code == 422
```

### TypeScript Testing (Jest/Vitest)
```typescript
// __tests__/components/TaskList.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { TaskList } from '@/components/TaskList'
import { api } from '@/lib/api'

jest.mock('@/lib/api')

describe('TaskList', () => {
  it('displays tasks when loaded', async () => {
    const mockTasks = [
      { id: 1, title: 'Task 1', completed: false },
      { id: 2, title: 'Task 2', completed: true }
    ]
    
    ;(api.getTasks as jest.Mock).mockResolvedValue(mockTasks)
    
    render(<TaskList userId="user-123" />)
    
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument()
      expect(screen.getByText('Task 2')).toBeInTheDocument()
    })
  })
  
  it('displays error message on failure', async () => {
    ;(api.getTasks as jest.Mock).mockRejectedValue(new Error('Network error'))
    
    render(<TaskList userId="user-123" />)
    
    await waitFor(() => {
      expect(screen.getByText(/failed to load tasks/i)).toBeInTheDocument()
    })
  })
})
```

### Test Organization
- **Arrange-Act-Assert**: Structure all tests with clear AAA pattern
- **One assertion per test**: Test one behavior per test case
- **Descriptive names**: Test names should describe the expected behavior
- **Test data factories**: Use factories for consistent test data generation
- **Mock external services**: Never call real APIs or databases in unit tests

---

## User Experience Standards

### Accessibility (WCAG 2.1 AA)
1. **Keyboard navigation**: All interactive elements accessible via keyboard
2. **Screen reader support**: Proper ARIA labels and semantic HTML
3. **Color contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
4. **Focus indicators**: Visible focus states for all interactive elements
5. **Alt text**: All images and icons must have descriptive alt text

### Design Consistency
```typescript
// Good: Use design system tokens
<button className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-md">
  Add Task
</button>

// Bad: Arbitrary values
<button className="bg-[#3B82F6] hover:bg-[#2563EB]">
  Add Task
</button>
```

### Responsive Design
- **Mobile-first**: Design for mobile, enhance for desktop
- **Breakpoints**: Use Tailwind's standard breakpoints (sm, md, lg, xl, 2xl)
- **Touch targets**: Minimum 44×44px for interactive elements
- **Viewport units**: Use rem/em for typography, avoid px when possible

### Loading States
```typescript
// Good: Explicit loading states
export function TaskList({ userId }: { userId: string }) {
  const { data: tasks, isLoading, error } = useTasks(userId)
  
  if (isLoading) return <TaskListSkeleton />
  if (error) return <TaskListError error={error} />
  if (!tasks?.length) return <EmptyState />
  
  return <div>{tasks.map(task => <TaskCard task={task} />)}</div>
}

// Bad: Generic loading
if (loading) return <div>Loading...</div>
```

### Error Messages
- **User-friendly**: No technical jargon in user-facing errors
- **Actionable**: Tell users what they can do to fix the issue
- **Contextual**: Errors appear near the relevant UI element
- **Consistent tone**: Friendly but professional language

---

## Performance Requirements

### Backend Performance
- **API response time**: 95th percentile < 200ms for CRUD operations
- **Database queries**: N+1 queries not allowed; use eager loading
- **Pagination**: Required for all list endpoints (default 20 items)
- **Caching**: Use Redis/in-memory cache for frequently accessed data
- **Connection pooling**: Minimum 5, maximum 20 database connections

### Frontend Performance
- **Lighthouse score**: Minimum 90 for Performance, Accessibility, Best Practices
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1
- **Bundle size**: Main bundle < 200KB gzipped

### Database Performance
```sql
-- Good: Indexed query
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
SELECT * FROM tasks WHERE user_id = $1;  -- Uses index

-- Bad: Table scan
SELECT * FROM tasks WHERE description LIKE '%meeting%';  -- Full table scan
```

### Optimization Strategies
1. **Code splitting**: Use dynamic imports for large components
2. **Image optimization**: Next.js Image component for all images
3. **API batching**: Combine related requests when possible
4. **Debouncing**: Debounce search inputs (300ms minimum)
5. **Virtual scrolling**: For lists with >100 items

---

## Security Standards

### Authentication & Authorization
- **JWT tokens**: Short-lived access tokens (15 min), refresh tokens (7 days)
- **HTTPS only**: All API communication over HTTPS in production
- **Password hashing**: bcrypt with minimum 10 rounds
- **Rate limiting**: Max 100 requests per minute per user
- **CORS**: Strict origin whitelisting

### Data Validation
```python
# Good: Input validation at API boundary
from pydantic import BaseModel, Field, validator

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

# Bad: No validation
def create_task(title, description):
    db.insert(title, description)  # SQL injection risk!
```

### API Security
- **SQL injection**: Use parameterized queries only
- **XSS prevention**: Sanitize all user input before rendering
- **CSRF protection**: Use CSRF tokens for state-changing operations
- **Secrets management**: Environment variables; never commit secrets
- **Dependency scanning**: Automated vulnerability scanning in CI

---

## Architecture Constraints

### Phase-Specific Rules

#### Phase I (Console App)
- **Pure Python**: No web frameworks
- **In-memory only**: No database or file persistence
- **Single file allowed**: Can be split for organization but not required

#### Phase II (Web App)
- **Monorepo structure**: Frontend and backend in separate folders
- **REST API only**: No GraphQL or other protocols
- **Neon Serverless**: Only allowed database
- **Better Auth**: Only allowed authentication library

#### Phase III (AI Chatbot)
- **OpenAI Agents SDK**: Required for AI logic
- **Official MCP SDK**: Required for MCP server
- **Stateless chat endpoint**: Server holds no conversation state
- **Database state**: Conversations and messages persisted to Neon

#### Phase IV (Local K8s)
- **Minikube only**: No kind, k3s, or other local clusters
- **Helm charts**: All deployments via Helm
- **kubectl-ai**: Required for AI-assisted operations
- **Docker Desktop**: Preferred container runtime

#### Phase V (Cloud K8s)
- **Managed K8s**: AKS, GKE, or OKE only
- **Kafka required**: Redpanda or Confluent Cloud
- **Dapr integration**: All building blocks (Pub/Sub, State, Secrets)
- **CI/CD pipeline**: GitHub Actions required

### Technology Constraints

#### Allowed
- **Languages**: Python 3.13+, TypeScript 5+, JavaScript (ES2023+)
- **Frameworks**: FastAPI, Next.js 15+ (App Router)
- **Databases**: Neon Serverless PostgreSQL only
- **AI**: OpenAI Agents SDK, Official MCP SDK
- **Cloud**: DigitalOcean, Google Cloud, Azure, Oracle Cloud
- **Containerization**: Docker, Kubernetes (Minikube, AKS, GKE, OKE)

#### Forbidden
- **Alternative ORMs**: No Prisma, TypeORM, raw SQL
- **Alternative auth**: No Auth0, Clerk, Supabase Auth
- **Alternative AI**: No LangChain, LlamaIndex, other frameworks
- **Alternative databases**: No MongoDB, Redis as primary DB
- **Alternative K8s**: No EKS, self-managed clusters

---

## Documentation Standards

### Code Documentation
```python
# Good: Complete function documentation
async def update_task(
    task_id: int,
    user_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Task:
    """
    Update an existing task's title and/or description.
    
    This function validates user ownership before allowing updates.
    At least one of title or description must be provided.
    
    Args:
        task_id: The ID of the task to update
        user_id: The ID of the user requesting the update
        title: New task title (1-200 characters) if provided
        description: New task description (max 1000 characters) if provided
        
    Returns:
        The updated Task object with new values
        
    Raises:
        TaskNotFoundError: If task_id doesn't exist
        UnauthorizedError: If user doesn't own the task
        ValueError: If both title and description are None
        
    Example:
        >>> task = await update_task(
        ...     task_id=123,
        ...     user_id="user-456",
        ...     title="Updated title"
        ... )
        >>> print(task.title)
        "Updated title"
    """
    pass
```

### Architecture Documentation
- **README.md**: Project overview, setup instructions, architecture summary
- **ARCHITECTURE.md**: Detailed system design, component relationships
- **API.md**: Complete API documentation with examples
- **DEPLOYMENT.md**: Production deployment instructions
- **CLAUDE.md**: Instructions for Claude Code and other AI agents

### Spec Documentation
- **speckit.constitution**: This file (principles and constraints)
- **speckit.specify**: What to build (requirements, user journeys, acceptance criteria)
- **speckit.plan**: How to build it (architecture, components, interfaces)
- **speckit.tasks**: Breakdown into actionable work units

---

## Git & Version Control

### Commit Standards
```bash
# Good commit messages
feat(tasks): add due date filtering to list endpoint
fix(auth): resolve JWT expiration edge case
docs(api): update task creation examples
test(tasks): add integration tests for update endpoint

# Bad commit messages
update stuff
fix bug
changes
wip
```

### Branching Strategy
- **main**: Production-ready code only
- **develop**: Integration branch for features
- **feature/\***: Individual feature branches
- **fix/\***: Bug fix branches
- **release/\***: Release preparation branches

### Pull Request Requirements
1. **Passes all tests**: CI must be green
2. **Spec reference**: Link to relevant spec sections
3. **Description**: Clear explanation of changes
4. **Screenshots**: For UI changes
5. **Breaking changes**: Clearly documented

---

## Continuous Integration

### Required CI Checks
1. **Linting**: Code passes all linters (ruff, eslint)
2. **Type checking**: mypy (Python), tsc (TypeScript)
3. **Unit tests**: Minimum 80% coverage
4. **Integration tests**: All API endpoints tested
5. **Security scan**: No critical vulnerabilities
6. **Build verification**: Application builds successfully

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  
  - repo: https://github.com/pre-commit/mirrors-eslint
    hooks:
      - id: eslint
        files: \.(js|jsx|ts|tsx)$
        args: [--fix]
```

---

## Monitoring & Observability

### Logging Standards
```python
# Good: Structured logging
import structlog

logger = structlog.get_logger()

logger.info(
    "task_created",
    task_id=task.id,
    user_id=user.id,
    title=task.title,
    duration_ms=42
)

# Bad: Print statements
print(f"Created task {task.id}")  # NEVER DO THIS
```

### Metrics to Track
- **Request rate**: Requests per second
- **Error rate**: Percentage of failed requests
- **Response time**: P50, P95, P99 latencies
- **Database query time**: Slow query detection (>100ms)
- **Cache hit rate**: Percentage of cached responses

---

## Exception Policy

### When to Deviate
Deviations from this constitution are allowed only when:

1. **Technically impossible**: The constraint cannot be met with available tools
2. **Spec-approved**: Deviation is documented in `speckit.specify` or `speckit.plan`
3. **Time-critical**: Hackathon deadline requires pragmatic trade-offs
4. **Documented**: Deviation is clearly documented with rationale

### Deviation Documentation
```markdown
## Deviation Log

### DEV-001: Using SQLite in Phase I
- **Date**: 2025-01-17
- **Reason**: Constitution requires "in-memory only" but testing CRUD operations easier with SQLite
- **Impact**: Low (only affects Phase I, replaced in Phase II)
- **Approval**: Self-approved (does not affect other phases)
```

---

## Enforcement

### Automated Enforcement
- **Pre-commit hooks**: Catch violations before commit
- **CI pipeline**: Block merges that violate standards
- **Code review**: Manual verification of complex rules

### Manual Enforcement
- **Spec reviews**: Verify specs meet constitution before implementation
- **Architecture reviews**: Verify plans align with constraints
- **Code reviews**: Ensure implementation follows standards

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-17 | Initial constitution |

---

## References

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Next.js Documentation](https://nextjs.org/docs)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Twelve-Factor App](https://12factor.net/)
