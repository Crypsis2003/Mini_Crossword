"""Authentication router."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserProfile, Token
from app.services.user_service import UserService
from app.services.stats_service import StatsService
from app.utils.auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_user_from_refresh_token,
)
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    logger.info(f"Registration attempt for username: {user_data.username}")
    user_service = UserService(db)
    user = user_service.create(user_data)
    logger.info(f"User registered successfully: {user.username}")
    return user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get JWT tokens."""
    logger.info(f"Login attempt for username: {credentials.username}")
    user_service = UserService(db)
    user = user_service.authenticate(credentials.username, credentials.password)

    if not user:
        logger.warning(f"Failed login attempt for username: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    logger.info(f"User logged in successfully: {user.username}")
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    user = get_user_from_refresh_token(refresh_token, db)

    access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return current_user


@router.get("/profile", response_model=UserProfile)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user profile with stats."""
    stats_service = StatsService(db)
    user_stats = stats_service.get_user_stats(current_user.id)
    friends_count = stats_service.get_friends_count(current_user.id)

    return UserProfile(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at,
        total_solves=user_stats["total_solves"],
        average_time_ms=user_stats["average_time_ms"],
        best_time_ms=user_stats["best_time_ms"],
        friends_count=friends_count,
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Logout (client should discard tokens)."""
    # JWT tokens are stateless, so we just acknowledge the logout
    # In production, you might want to blacklist the token
    logger.info(f"User logged out: {current_user.username}")
    return {"message": "Successfully logged out"}
