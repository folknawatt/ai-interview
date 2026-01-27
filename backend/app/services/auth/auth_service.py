"""
Authentication Service.

Handles user authentication, password hashing, and JWT token management.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from sqlmodel import Session, select

from app.config.settings import settings
from app.database.models import HRUser, UserRole
from app.exceptions import NotFoundError, ValidationError

# JWT Settings
SECRET_KEY = settings.jwt_secret_key or "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + \
                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            raise ValidationError(f"Invalid token: {str(e)}") from e

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[HRUser]:
        """Get user by username."""
        return session.exec(
            select(HRUser).where(HRUser.username == username)
        ).first()

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[HRUser]:
        """Get user by ID."""
        return session.exec(
            select(HRUser).where(HRUser.id == user_id)
        ).first()

    @staticmethod
    def authenticate_user(session: Session, username: str, password: str) -> HRUser:
        """Authenticate a user with username and password."""
        user = AuthService.get_user_by_username(session, username)
        if not user:
            raise NotFoundError("User not found")
        if not AuthService.verify_password(password, user.hashed_password):
            raise ValidationError("Incorrect password")
        if not user.is_active:
            raise ValidationError("User is inactive")
        return user

    @staticmethod
    def create_user(
        session: Session,
        username: str,
        email: str,
        password: str,
        full_name: str,
        role: UserRole = UserRole.HR
    ) -> HRUser:
        """Create a new user."""
        # Check if username already exists
        existing = session.exec(
            select(HRUser).where(HRUser.username == username)
        ).first()
        if existing:
            raise ValidationError("Username already exists")

        # Check if email already exists
        existing_email = session.exec(
            select(HRUser).where(HRUser.email == email)
        ).first()
        if existing_email:
            raise ValidationError("Email already exists")

        # Create user
        user = HRUser(
            username=username,
            email=email,
            hashed_password=AuthService.get_password_hash(password),
            full_name=full_name,
            role=role,
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def create_default_admin(session: Session) -> Optional[HRUser]:
        """Create default admin user if not exists."""
        existing = AuthService.get_user_by_username(session, "admin")
        if existing:
            return None  # Admin already exists

        return AuthService.create_user(
            session=session,
            username="admin",
            email="admin@ai-interview.com",
            password="password",  # Change this in production!
            full_name="Administrator",
            role=UserRole.ADMIN
        )
