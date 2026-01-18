# Todo Backend

FastAPI backend for Phase II of "The Evolution of Todo" web application.

## Features

- RESTful API for task CRUD operations
- JWT authentication with refresh tokens
- PostgreSQL database with SQLModel ORM
- Async operations with asyncpg
- Database migrations with Alembic

## Development

```bash
# Install dependencies
uv sync

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload

# Run tests
uv run pytest
```

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Logout
- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `POST /api/tasks/{id}/done` - Mark done
- `POST /api/tasks/{id}/pending` - Mark pending
