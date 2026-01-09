"""Puzzle-related Pydantic schemas."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ClueItem(BaseModel):
    """Schema for a single clue."""

    number: int
    clue: str
    length: int
    row: int
    col: int


class PuzzleBase(BaseModel):
    """Base puzzle schema."""

    title: str
    size: int = Field(..., ge=5, le=7)
    difficulty: str = "medium"


class PuzzleCreate(PuzzleBase):
    """Schema for creating a puzzle."""

    grid: list[list[str]]  # Grid with '.' for blocks and ' ' for empty cells
    solution: list[list[str]]  # Solution grid
    clues_across: list[ClueItem]
    clues_down: list[ClueItem]
    scheduled_date: Optional[date] = None


class PuzzleResponse(PuzzleBase):
    """Schema for puzzle response (admin view with solution)."""

    id: int
    grid: list[list[str]]
    solution: list[list[str]]
    clues_across: list[ClueItem]
    clues_down: list[ClueItem]
    scheduled_date: Optional[date] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PuzzlePlay(BaseModel):
    """Schema for puzzle play (without solution)."""

    id: int
    title: str
    size: int
    difficulty: str
    scheduled_date: Optional[date] = None
    grid: list[list[str]]  # Grid layout showing blocks
    clues_across: list[ClueItem]
    clues_down: list[ClueItem]

    model_config = {"from_attributes": True}


class PuzzleCheck(BaseModel):
    """Schema for checking puzzle answers."""

    puzzle_id: int
    grid: list[list[str]]  # User's current grid state


class PuzzleCheckResponse(BaseModel):
    """Response for puzzle check."""

    is_correct: bool
    incorrect_cells: list[tuple[int, int]] = []  # List of (row, col) for incorrect cells
