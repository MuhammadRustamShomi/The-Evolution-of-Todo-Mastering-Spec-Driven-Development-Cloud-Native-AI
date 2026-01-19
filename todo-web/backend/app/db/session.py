"""Database session configuration."""

import os
import re
from collections.abc import AsyncGenerator
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from app.config import get_settings

settings = get_settings()


def fix_asyncpg_url(database_url: str) -> str:
    """Fix PostgreSQL URL for asyncpg compatibility.

    asyncpg doesn't accept 'sslmode' parameter - it uses 'ssl' instead.
    This function converts sslmode=require to ssl=require for asyncpg.
    """
    if "asyncpg" not in database_url:
        return database_url

    parsed = urlparse(database_url)
    if not parsed.query:
        return database_url

    # Parse query parameters
    params = parse_qs(parsed.query)

    # Convert sslmode to ssl for asyncpg
    if "sslmode" in params:
        sslmode_value = params.pop("sslmode")[0]
        # asyncpg uses ssl=true or ssl parameter differently
        # For most cases, sslmode=require translates to ssl=require
        params["ssl"] = [sslmode_value]

    # Rebuild the URL
    new_query = urlencode(params, doseq=True)
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)

# Use NullPool for serverless environments (Vercel, AWS Lambda, etc.)
# This prevents connection pool issues in ephemeral compute
is_serverless = os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")

engine_kwargs = {
    "echo": settings.debug,
    "future": True,
}

if is_serverless:
    # Serverless: disable connection pooling (database handles it)
    engine_kwargs["poolclass"] = NullPool
else:
    # Traditional server: use connection pooling
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = 5
    engine_kwargs["max_overflow"] = 10

# Fix the database URL for asyncpg compatibility
database_url = fix_asyncpg_url(settings.database_url)
engine = create_async_engine(database_url, **engine_kwargs)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db_and_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
