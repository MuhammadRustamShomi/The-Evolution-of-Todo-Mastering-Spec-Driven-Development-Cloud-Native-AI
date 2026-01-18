"""User model for authentication."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base user fields."""

    email: EmailStr = Field(index=True, unique=True)
    name: Optional[str] = None


class User(UserBase, table=True):
    """User database model."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(SQLModel):
    """User creation schema."""

    email: EmailStr
    password: str
    name: Optional[str] = None


class UserRead(UserBase):
    """User response schema."""

    id: UUID
    email_verified: bool
    created_at: datetime
