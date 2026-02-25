"""Authentication Schemas.

Pydantic schemas for authentication requests and responses.
"""

from pydantic import BaseModel, EmailStr

from app.database.models import UserRole


class LoginRequest(BaseModel):
    """Login request payload."""

    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response with user info. Token is delivered via HttpOnly cookie."""

    access_token: str | None = (
        None  # Kept for Swagger/Bearer fallback; None when cookie auth is used
    )
    token_type: str = "bearer"
    user: "UserResponse"


class RegisterRequest(BaseModel):
    """Register new user request."""

    username: str
    email: EmailStr
    password: str
    full_name: str
    role: UserRole | None = UserRole.HR


class UserResponse(BaseModel):
    """User information response."""

    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """Token payload data."""

    user_id: int
    username: str
    role: UserRole


# Update forward references
LoginResponse.model_rebuild()
