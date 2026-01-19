"""Vercel serverless entry point for FastAPI application."""

try:
    from app.main import app
except Exception as e:
    # Fallback app if main app fails to load
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    @app.get("/health")
    @app.get("/api/health")
    def error_handler():
        return {"error": str(e), "status": "failed_to_load"}

# Export the FastAPI app for Vercel
# Vercel will handle this as an ASGI application
