"""Puzzle service for puzzle-related business logic."""

import json
import hashlib
from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.puzzle import Puzzle
from app.schemas.puzzle import PuzzleCreate, ClueItem


class PuzzleService:
    """Service class for puzzle operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, puzzle_id: int) -> Optional[Puzzle]:
        """Get puzzle by ID."""
        return self.db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()

    def get_by_date(self, puzzle_date: date) -> Optional[Puzzle]:
        """Get puzzle scheduled for a specific date."""
        return self.db.query(Puzzle).filter(Puzzle.scheduled_date == puzzle_date).first()

    def get_today_puzzle(self) -> Optional[Puzzle]:
        """Get today's puzzle."""
        today = date.today()

        # First, try to get a puzzle specifically scheduled for today
        puzzle = self.get_by_date(today)
        if puzzle:
            return puzzle

        # If no puzzle is scheduled for today, select one deterministically
        # based on the date (rotation through unscheduled puzzles)
        unscheduled_puzzles = (
            self.db.query(Puzzle)
            .filter(Puzzle.scheduled_date == None)
            .order_by(Puzzle.id)
            .all()
        )

        if not unscheduled_puzzles:
            return None

        # Use date-based deterministic selection
        date_hash = int(hashlib.md5(today.isoformat().encode()).hexdigest(), 16)
        index = date_hash % len(unscheduled_puzzles)

        return unscheduled_puzzles[index]

    def create(self, puzzle_data: PuzzleCreate) -> Puzzle:
        """Create a new puzzle."""
        # Check if a puzzle is already scheduled for the same date
        if puzzle_data.scheduled_date:
            existing = self.get_by_date(puzzle_data.scheduled_date)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A puzzle is already scheduled for {puzzle_data.scheduled_date}",
                )

        # Serialize grid and clues to JSON
        puzzle = Puzzle(
            title=puzzle_data.title,
            size=puzzle_data.size,
            difficulty=puzzle_data.difficulty,
            grid=json.dumps(puzzle_data.grid),
            solution=json.dumps(puzzle_data.solution),
            clues_across=json.dumps([clue.model_dump() for clue in puzzle_data.clues_across]),
            clues_down=json.dumps([clue.model_dump() for clue in puzzle_data.clues_down]),
            scheduled_date=puzzle_data.scheduled_date,
        )

        self.db.add(puzzle)
        self.db.commit()
        self.db.refresh(puzzle)

        return puzzle

    def parse_puzzle(self, puzzle: Puzzle) -> dict:
        """Parse puzzle JSON fields into Python objects."""
        return {
            "id": puzzle.id,
            "title": puzzle.title,
            "size": puzzle.size,
            "difficulty": puzzle.difficulty,
            "scheduled_date": puzzle.scheduled_date,
            "grid": json.loads(puzzle.grid),
            "solution": json.loads(puzzle.solution),
            "clues_across": [ClueItem(**c) for c in json.loads(puzzle.clues_across)],
            "clues_down": [ClueItem(**c) for c in json.loads(puzzle.clues_down)],
            "created_at": puzzle.created_at,
        }

    def check_solution(self, puzzle: Puzzle, user_grid: list[list[str]]) -> tuple[bool, list[tuple[int, int]]]:
        """Check user's solution against the puzzle solution.

        Returns:
            tuple: (is_correct, list of incorrect cell positions)
        """
        solution = json.loads(puzzle.solution)
        incorrect_cells = []

        for row in range(puzzle.size):
            for col in range(puzzle.size):
                solution_cell = solution[row][col].upper()
                user_cell = user_grid[row][col].upper() if row < len(user_grid) and col < len(user_grid[row]) else ""

                # Skip blocked cells (marked with '.')
                if solution_cell == ".":
                    continue

                if user_cell != solution_cell:
                    incorrect_cells.append((row, col))

        return len(incorrect_cells) == 0, incorrect_cells

    def get_all_puzzles(self, skip: int = 0, limit: int = 100) -> list[Puzzle]:
        """Get all puzzles with pagination."""
        return self.db.query(Puzzle).offset(skip).limit(limit).all()

    def schedule_puzzle(self, puzzle_id: int, scheduled_date: date) -> Puzzle:
        """Schedule a puzzle for a specific date."""
        puzzle = self.get_by_id(puzzle_id)
        if not puzzle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Puzzle not found",
            )

        # Check if date is already taken
        existing = self.get_by_date(scheduled_date)
        if existing and existing.id != puzzle_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A puzzle is already scheduled for {scheduled_date}",
            )

        puzzle.scheduled_date = scheduled_date
        self.db.commit()
        self.db.refresh(puzzle)

        return puzzle
