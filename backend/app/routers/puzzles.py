"""Puzzles router."""

import logging
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.puzzle import PuzzlePlay, PuzzleCreate, PuzzleResponse
from app.schemas.solve import SolveCreate, SolveResult
from app.services.puzzle_service import PuzzleService
from app.services.stats_service import StatsService
from app.services.puzzle_cache import ensure_weekly_cache
from app.utils.auth import get_current_user, get_current_user_optional
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.get("/all")
def list_all_puzzles(db: Session = Depends(get_db)):
    """List all puzzles (admin/debug endpoint)."""
    from app.models.puzzle import Puzzle
    puzzles = db.query(Puzzle).order_by(Puzzle.scheduled_date).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "size": p.size,
            "difficulty": p.difficulty,
            "scheduled_date": str(p.scheduled_date) if p.scheduled_date else None,
            "week_key": p.week_key,
        }
        for p in puzzles
    ]


@router.post("/refresh")
def refresh_puzzles(db: Session = Depends(get_db)):
    """Force refresh puzzles for current week. Hit this endpoint to regenerate."""
    from app.models.puzzle import Puzzle
    from app.models.cache_meta import PuzzleCacheMeta
    from app.services.puzzle_cache import get_current_week_key, ensure_weekly_cache

    week_key = get_current_week_key()

    # Delete existing puzzles and cache meta for this week
    deleted_puzzles = db.query(Puzzle).filter(Puzzle.week_key == week_key).delete()
    deleted_meta = db.query(PuzzleCacheMeta).filter(PuzzleCacheMeta.week_key == week_key).delete()
    db.commit()

    # Regenerate
    ensure_weekly_cache(db)

    # Get new puzzles
    puzzles = db.query(Puzzle).filter(Puzzle.week_key == week_key).order_by(Puzzle.scheduled_date).all()

    return {
        "success": True,
        "week_key": week_key,
        "deleted_puzzles": deleted_puzzles,
        "new_puzzles": len(puzzles),
        "puzzles": [
            {"id": p.id, "date": str(p.scheduled_date), "title": p.title}
            for p in puzzles
        ]
    }


@router.get("/today", response_model=PuzzlePlay)
def get_today_puzzle(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Get today's puzzle (playable version without solution)."""
    # Ensure weekly cache is populated (auto-generates if missing)
    ensure_weekly_cache(db)

    puzzle_service = PuzzleService(db)
    puzzle = puzzle_service.get_today_puzzle()

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No puzzle available for today",
        )

    parsed = puzzle_service.parse_puzzle(puzzle)

    # Return without solution
    return PuzzlePlay(
        id=parsed["id"],
        title=parsed["title"],
        size=parsed["size"],
        difficulty=parsed["difficulty"],
        scheduled_date=parsed["scheduled_date"],
        grid=parsed["grid"],
        clues_across=parsed["clues_across"],
        clues_down=parsed["clues_down"],
    )


@router.get("/date/{puzzle_date}", response_model=PuzzlePlay)
def get_puzzle_by_date(
    puzzle_date: date,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Get puzzle for a specific date."""
    puzzle_service = PuzzleService(db)
    puzzle = puzzle_service.get_by_date(puzzle_date)

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No puzzle found for {puzzle_date}",
        )

    parsed = puzzle_service.parse_puzzle(puzzle)

    return PuzzlePlay(
        id=parsed["id"],
        title=parsed["title"],
        size=parsed["size"],
        difficulty=parsed["difficulty"],
        scheduled_date=parsed["scheduled_date"],
        grid=parsed["grid"],
        clues_across=parsed["clues_across"],
        clues_down=parsed["clues_down"],
    )


@router.get("/practice/random", response_model=PuzzlePlay)
def get_practice_puzzle(
    exclude: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Get a random puzzle for practice mode (not recorded on leaderboard)."""
    puzzle_service = PuzzleService(db)

    # If no exclude specified, exclude today's puzzle
    if exclude is None:
        today_puzzle = puzzle_service.get_today_puzzle()
        exclude = today_puzzle.id if today_puzzle else None

    puzzle = puzzle_service.get_random_practice_puzzle(exclude_puzzle_id=exclude)

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No practice puzzles available",
        )

    parsed = puzzle_service.parse_puzzle(puzzle)

    return PuzzlePlay(
        id=parsed["id"],
        title=parsed["title"],
        size=parsed["size"],
        difficulty=parsed["difficulty"],
        scheduled_date=parsed["scheduled_date"],
        grid=parsed["grid"],
        clues_across=parsed["clues_across"],
        clues_down=parsed["clues_down"],
    )


@router.get("/{puzzle_id}", response_model=PuzzlePlay)
def get_puzzle(
    puzzle_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Get a specific puzzle by ID."""
    puzzle_service = PuzzleService(db)
    puzzle = puzzle_service.get_by_id(puzzle_id)

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puzzle not found",
        )

    parsed = puzzle_service.parse_puzzle(puzzle)

    return PuzzlePlay(
        id=parsed["id"],
        title=parsed["title"],
        size=parsed["size"],
        difficulty=parsed["difficulty"],
        scheduled_date=parsed["scheduled_date"],
        grid=parsed["grid"],
        clues_across=parsed["clues_across"],
        clues_down=parsed["clues_down"],
    )


@router.post("/{puzzle_id}/check")
def check_puzzle(
    puzzle_id: int,
    grid: list[list[str]],
    db: Session = Depends(get_db),
):
    """Check if the submitted grid is correct."""
    puzzle_service = PuzzleService(db)
    puzzle = puzzle_service.get_by_id(puzzle_id)

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puzzle not found",
        )

    is_correct, incorrect_cells = puzzle_service.check_solution(puzzle, grid)

    return {
        "is_correct": is_correct,
        "incorrect_cells": incorrect_cells,
    }


@router.post("/{puzzle_id}/solve", response_model=SolveResult)
def submit_solve(
    puzzle_id: int,
    solve_data: SolveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a completed puzzle solve."""
    if solve_data.puzzle_id != puzzle_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Puzzle ID mismatch",
        )

    stats_service = StatsService(db)
    puzzle_service = PuzzleService(db)

    try:
        solve, is_new_record, rank = stats_service.submit_solve(
            user_id=current_user.id,
            puzzle_id=puzzle_id,
            time_ms=solve_data.time_ms,
            user_grid=solve_data.grid,
        )

        # Generate share text
        puzzle = puzzle_service.get_by_id(puzzle_id)
        share_text = stats_service.generate_share_text(
            puzzle=puzzle,
            time_ms=solve.time_ms,
            puzzle_date=puzzle.scheduled_date,
        )

        logger.info(f"User {current_user.username} solved puzzle {puzzle_id} in {solve.time_ms}ms")

        return SolveResult(
            success=True,
            message="Puzzle solved successfully!",
            time_ms=solve.time_ms,
            rank=rank,
            is_new_record=is_new_record,
            share_text=share_text,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting solve: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error submitting solve",
        )


@router.get("/{puzzle_id}/my-solve")
def get_my_solve(
    puzzle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current user's solve for a puzzle."""
    stats_service = StatsService(db)
    solve = stats_service.get_solve(current_user.id, puzzle_id)

    if not solve:
        return {"solved": False}

    return {
        "solved": True,
        "time_ms": solve.time_ms,
        "completed_at": solve.completed_at,
        "attempt_count": solve.attempt_count,
    }


@router.get("/{puzzle_id}/solution")
def get_puzzle_solution(
    puzzle_id: int,
    db: Session = Depends(get_db),
):
    """Get puzzle solution (for reveal functionality)."""
    puzzle_service = PuzzleService(db)
    puzzle = puzzle_service.get_by_id(puzzle_id)

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puzzle not found",
        )

    parsed = puzzle_service.parse_puzzle(puzzle)

    return {
        "solution": parsed["solution"],
    }
