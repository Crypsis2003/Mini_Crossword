"""User service for user-related business logic."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password


class UserService:
    """Service class for user operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username.lower()).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email.lower()).first()

    def create(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if username already exists
        if self.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        # Check if email already exists
        if self.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create user with hashed password
        user = User(
            username=user_data.username.lower(),
            email=user_data.email.lower(),
            hashed_password=hash_password(user_data.password),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        user = self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def update_password(self, user: User, new_password: str) -> User:
        """Update user password."""
        user.hashed_password = hash_password(new_password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def deactivate(self, user: User) -> User:
        """Deactivate user account."""
        user.is_active = False
        self.db.commit()
        self.db.refresh(user)
        return user

    def search_users(self, query: str, limit: int = 10) -> list[User]:
        """Search users by username."""
        return (
            self.db.query(User)
            .filter(User.username.ilike(f"%{query}%"))
            .filter(User.is_active == True)
            .limit(limit)
            .all()
        )
