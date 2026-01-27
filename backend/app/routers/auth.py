"""
Authentication Router.

Provides endpoints for user authentication:
- POST /auth/login - Authenticate user and return JWT
- POST /auth/register - Create new user (admin only)
- GET /auth/me - Get current user info
"""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database import get_db
from app.database.models import HRUser, UserRole
from app.exceptions import NotFoundError, ValidationError
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_db)
) -> HRUser:
    """Dependency to get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = AuthService.decode_token(token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except ValidationError:
        raise credentials_exception

    user = AuthService.get_user_by_id(session, user_id)
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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db)
):
    """Authenticate user and return JWT token."""
    try:
        user = AuthService.authenticate_user(
            session, form_data.username, form_data.password
        )
    except (NotFoundError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    # Create token
    access_token = AuthService.create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "role": user.role.value
        }
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/register", response_model=UserResponse)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_db),
    current_user: HRUser = Depends(require_role(UserRole.ADMIN))
):
    """Register a new user. Admin only."""
    try:
        user = AuthService.create_user(
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
async def init_admin(session: Session = Depends(get_db)):
    """Initialize default admin user. For initial setup only."""
    user = AuthService.create_default_admin(session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user already exists"
        )
    return UserResponse.model_validate(user)
