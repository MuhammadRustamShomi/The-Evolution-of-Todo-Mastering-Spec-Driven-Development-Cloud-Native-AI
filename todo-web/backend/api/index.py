"""Vercel serverless entry point for FastAPI application."""

from app.main import app

# Export the FastAPI app for Vercel
# Vercel will handle this as an ASGI application
