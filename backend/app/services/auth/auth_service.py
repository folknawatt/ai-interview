"""Authentication Service.

Handles user authentication, password hashing, and JWT token management.
"""

from datetime import UTC, datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.config.settings import settings
from app.database.models import HRUser, UserRole
from app.exceptions import NotFoundError, ValidationError


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(
                token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
            )
            return payload
        except JWTError as e:
            raise ValidationError(f"Invalid token: {str(e)}") from e

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> HRUser | None:
        """Get user by username."""
        result = await session.exec(select(HRUser).where(HRUser.username == username))
        return result.first()

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> HRUser | None:
        """Get user by ID."""
        result = await session.exec(select(HRUser).where(HRUser.id == user_id))
        return result.first()

    @staticmethod
    async def authenticate_user(session: AsyncSession, username: str, password: str) -> HRUser:
        """Authenticate a user with username and password."""
        user = await AuthService.get_user_by_username(session, username)
        if not user:
            raise NotFoundError("User not found")
        if not AuthService.verify_password(password, user.hashed_password):
            raise ValidationError("Incorrect password")
        if not user.is_active:
            raise ValidationError("User is inactive")
        return user

    @staticmethod
    async def create_user(
        session: AsyncSession,
        username: str,
        email: str,
        password: str,
        full_name: str,
        role: UserRole = UserRole.HR,
    ) -> HRUser:
        """Create a new user."""
        # Check if username already exists
        result_username = await session.exec(select(HRUser).where(HRUser.username == username))
        if result_username.first():
            raise ValidationError("Username already exists")

        # Check if email already exists
        result_email = await session.exec(select(HRUser).where(HRUser.email == email))
        if result_email.first():
            raise ValidationError("Email already exists")

        # Create user
        user = HRUser(
            username=username,
            email=email,
            hashed_password=AuthService.get_password_hash(password),
            full_name=full_name,
            role=role,
            is_active=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def create_default_admin(session: AsyncSession) -> HRUser | None:
        """Create or update default admin user."""
        admin_email = settings.admin_default_email
        admin_password = settings.admin_default_password

        # Check by username
        existing = await AuthService.get_user_by_username(session, "admin")

        if existing:
            # Update password if exists (Force Reset)
            new_hash = AuthService.get_password_hash(admin_password)
            existing.hashed_password = new_hash
            existing.email = admin_email  # Also update email if it changed in settings
            session.add(existing)
            await session.commit()
            await session.refresh(existing)
            return existing

        return await AuthService.create_user(
            session=session,
            username="admin",
            email=admin_email,
            password=admin_password,
            full_name="Administrator",
            role=UserRole.ADMIN,
        )
