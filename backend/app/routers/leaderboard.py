"""Leaderboard router."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.solve import LeaderboardResponse, LeaderboardEntry
from app.services.puzzle_service import PuzzleService
from app.services.stats_service import StatsService
from app.utils.auth import get_current_user, get_current_user_optional
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/today", response_model=LeaderboardResponse)
def get_today_leaderboard(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Get leaderboard for today's puzzle."""
    puzzle_service = PuzzleService(db)
    stats_service = StatsService(db)

    puzzle = puzzle_service.get_today_puzzle()
    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No puzzle available for today",
        )

    current_user_id = current_user.id if current_user else None

    # Get global leaderboard
    global_entries = stats_service.get_puzzle_leaderboard(
        puzzle.id,
        limit=50,
        current_user_id=current_user_id,
    )

    # Get user's entry
    user_entry = None
    friends_entries = []

    if current_user:
        solve = stats_service.get_solve(current_user.id, puzzle.id)
        if solve:
            rank = stats_service.get_user_rank(current_user.id, puzzle.id)
            user_entry = LeaderboardEntry(
                rank=rank,
                user_id=current_user.id,
                username=current_user.username,
                time_ms=solve.time_ms,
                completed_at=solve.completed_at,
                is_friend=False,
                is_current_user=True,
            )

        # Get friends leaderboard
        friends_data = stats_service.get_friends_leaderboard(current_user.id, puzzle.id)
        friends_entries = [LeaderboardEntry(**entry) for entry in friends_data]

    return LeaderboardResponse(
        puzzle_id=puzzle.id,
        puzzle_title=puzzle.title,
        puzzle_date=puzzle.scheduled_date.isoformat() if puzzle.scheduled_date else None,
        entries=[LeaderboardEntry(**entry) for entry in global_entries],
        user_entry=user_entry,
        friends_entries=friends_entries,
    )


@router.get("/puzzle/{puzzle_id}", response_model=LeaderboardResponse)
def get_puzzle_leaderboard(
    puzzle_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Get leaderboard for a specific puzzle."""
    puzzle_service = PuzzleService(db)
    stats_service = StatsService(db)

    puzzle = puzzle_service.get_by_id(puzzle_id)
    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puzzle not found",
        )

    current_user_id = current_user.id if current_user else None

    # Get global leaderboard
    global_entries = stats_service.get_puzzle_leaderboard(
        puzzle.id,
        limit=50,
        current_user_id=current_user_id,
    )

    # Get user's entry
    user_entry = None
    friends_entries = []

    if current_user:
        solve = stats_service.get_solve(current_user.id, puzzle.id)
        if solve:
            rank = stats_service.get_user_rank(current_user.id, puzzle.id)
            user_entry = LeaderboardEntry(
                rank=rank,
                user_id=current_user.id,
                username=current_user.username,
                time_ms=solve.time_ms,
                completed_at=solve.completed_at,
                is_friend=False,
                is_current_user=True,
            )

        # Get friends leaderboard
        friends_data = stats_service.get_friends_leaderboard(current_user.id, puzzle.id)
        friends_entries = [LeaderboardEntry(**entry) for entry in friends_data]

    return LeaderboardResponse(
        puzzle_id=puzzle.id,
        puzzle_title=puzzle.title,
        puzzle_date=puzzle.scheduled_date.isoformat() if puzzle.scheduled_date else None,
        entries=[LeaderboardEntry(**entry) for entry in global_entries],
        user_entry=user_entry,
        friends_entries=friends_entries,
    )


@router.get("/friends/today")
def get_friends_today_leaderboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get friends-only leaderboard for today's puzzle."""
    puzzle_service = PuzzleService(db)
    stats_service = StatsService(db)

    puzzle = puzzle_service.get_today_puzzle()
    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No puzzle available for today",
        )

    friends_data = stats_service.get_friends_leaderboard(current_user.id, puzzle.id)

    return {
        "puzzle_id": puzzle.id,
        "puzzle_title": puzzle.title,
        "entries": friends_data,
    }
