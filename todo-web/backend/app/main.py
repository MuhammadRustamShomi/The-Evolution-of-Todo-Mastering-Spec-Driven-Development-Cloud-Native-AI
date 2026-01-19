"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.session import create_db_and_tables
from app.routers import auth, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await create_db_and_tables()
    yield
    # Shutdown (cleanup if needed)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "running",
            "endpoints": {
                "health": "/health",
                "ready": "/ready",
                "docs": "/docs",
                "auth": "/api/auth",
                "tasks": "/api/tasks",
            },
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}

    @app.get("/ready")
    async def readiness_check():
        """Readiness check endpoint."""
        return {"status": "ready"}

    return app


app = create_app()
