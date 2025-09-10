"""User model for authentication and profile management"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """User profile model"""

    email: EmailStr
    name: Optional[str] = None
    created_at: datetime


class UserResponse(BaseModel):
    """User response model (without sensitive data)"""

    id: str
    email: EmailStr
    name: Optional[str] = None
    created_at: datetime


class UserUpdate(BaseModel):
    """User update model"""

    name: Optional[str] = None


class UserCreate(BaseModel):
    """User creation model"""

    email: EmailStr
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model"""

    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Authentication response model"""

    message: str
    user: UserResponse
    token: str
