"""Solve-related Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SolveCreate(BaseModel):
    """Schema for submitting a solve."""

    puzzle_id: int
    time_ms: int = Field(..., gt=0)  # Time must be positive
    grid: list[list[str]]  # Final grid state for verification
    hints_used: int = Field(default=0, ge=0)  # Number of hints used


class SolveResponse(BaseModel):
    """Schema for solve response."""

    id: int
    user_id: int
    puzzle_id: int
    time_ms: int
    completed_at: datetime
    is_completed: bool
    attempt_count: int
    hints_used: int = 0

    model_config = {"from_attributes": True}


class SolveResult(BaseModel):
    """Schema for solve submission result."""

    success: bool
    message: str
    time_ms: Optional[int] = None
    rank: Optional[int] = None
    is_new_record: bool = False
    share_text: Optional[str] = None
    hints_used: int = 0


class LeaderboardEntry(BaseModel):
    """Schema for a leaderboard entry."""

    rank: int
    user_id: int
    username: str
    time_ms: int
    completed_at: datetime
    is_friend: bool = False
    is_current_user: bool = False
    hints_used: int = 0


class LeaderboardResponse(BaseModel):
    """Schema for leaderboard response."""

    puzzle_id: int
    puzzle_title: str
    puzzle_date: Optional[str] = None
    entries: list[LeaderboardEntry]
    user_entry: Optional[LeaderboardEntry] = None
    friends_entries: list[LeaderboardEntry] = []
