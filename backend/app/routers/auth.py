"""
Authentication Router.

Provides endpoints for user authentication:
- POST /auth/login - Authenticate user and return JWT
- POST /auth/register - Create new user (admin only)
- GET /auth/me - Get current user info
"""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import settings

from app.database.db import get_db
from app.database.models import HRUser, UserRole
from app.exceptions import NotFoundError, ValidationError
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# We still keep OAuth2PasswordBearer for Swagger UI support,
# but we'll make it optional since we primarily use cookies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def get_current_user(
    request: Request,
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
    session: AsyncSession = Depends(get_db)
) -> HRUser:
    """
    Dependency to get current authenticated user.
    Prioritizes HttpOnly Cookie, falls back to Bearer token (for testing/Swagger).
    """
    # 1. Try to get from Cookie
    cookie_token = request.cookies.get("access_token")

    # 2. Use cookie token if available, otherwise use Bearer token
    final_token = cookie_token if cookie_token else token

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not final_token:
        raise credentials_exception

    try:
        payload = AuthService.decode_token(final_token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except ValidationError:
        raise credentials_exception

    user = await AuthService.get_user_by_id(session, user_id)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    return user


def require_role(*roles: UserRole):
    """Factory for role-checking dependency."""
    async def role_checker(current_user: HRUser = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {', '.join(r.value for r in roles)}"
            )
        return current_user
    return role_checker


@router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db)
):
    """Authenticate user and set HttpOnly cookies."""
    try:
        user = await AuthService.authenticate_user(
            session, form_data.username, form_data.password
        )
    except (NotFoundError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    # Create access token
    access_token = AuthService.create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "role": user.role.value
        },
        expires_delta=timedelta(
            minutes=settings.jwt_access_token_expire_minutes)
    )

    # Create refresh token (can be longer lived)
    refresh_token = AuthService.create_access_token(
        data={"user_id": user.id, "type": "refresh"},
        expires_delta=timedelta(days=settings.jwt_refresh_token_expire_days)
    )

    # Set HttpOnly Cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        max_age=settings.jwt_access_token_expire_minutes * 60
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        max_age=settings.jwt_refresh_token_expire_days * 24 * 60 * 60
    )

    return LoginResponse(
        # Token is now in cookie, returning empty string or just "logged_in" to satisfy schema
        access_token="",
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/logout")
async def logout(response: Response):
    """Logout user by clearing cookies."""
    response.delete_cookie(
        key="access_token",
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain
    )
    response.delete_cookie(
        key="refresh_token",
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain
    )
    return {"message": "Logged out successfully"}


@router.post("/register", response_model=UserResponse)
async def register(
    request: RegisterRequest,
    session: AsyncSession = Depends(get_db),
    current_user: HRUser = Depends(require_role(UserRole.ADMIN))
):
    """Register a new user. Admin only."""
    try:
        user = await AuthService.create_user(
            session=session,
            username=request.username,
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            role=request.role or UserRole.HR
        )
        return UserResponse.model_validate(user)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: HRUser = Depends(get_current_user)):
    """Get current authenticated user info."""
    return UserResponse.model_validate(current_user)


@router.post("/init-admin", response_model=UserResponse, include_in_schema=False)
async def init_admin(session: AsyncSession = Depends(get_db)):
    """Initialize default admin user. For initial setup only."""
    user = await AuthService.create_default_admin(session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user already exists"
        )
    return UserResponse.model_validate(user)
