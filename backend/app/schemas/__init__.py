"""Pydantic schemas for request/response validation."""

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserProfile,
    Token,
    TokenPayload,
)
from app.schemas.puzzle import (
    PuzzleBase,
    PuzzleCreate,
    PuzzleResponse,
    PuzzlePlay,
    ClueItem,
)
from app.schemas.solve import (
    SolveCreate,
    SolveResponse,
    SolveResult,
)
from app.schemas.friend import (
    FriendRequestCreate,
    FriendRequestResponse,
    FriendResponse,
    FriendRequestAction,
)

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserProfile",
    "Token",
    "TokenPayload",
    "PuzzleBase",
    "PuzzleCreate",
    "PuzzleResponse",
    "PuzzlePlay",
    "ClueItem",
    "SolveCreate",
    "SolveResponse",
    "SolveResult",
    "FriendRequestCreate",
    "FriendRequestResponse",
    "FriendResponse",
    "FriendRequestAction",
]
