"""Vercel serverless entry point for FastAPI application."""

import os
import sys

# Try to load the full app
try:
    from app.main import app
except Exception as e:
    # If main app fails, create fallback with error info
    from fastapi import FastAPI
    app = FastAPI()
    error_msg = str(e)
    error_type = type(e).__name__

    @app.get("/")
    @app.get("/health")
    def error_info():
        return {
            "error": error_msg,
            "type": error_type,
            "python_version": sys.version,
            "env_vars": list(os.environ.keys()),
        }
