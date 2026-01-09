"""Stats service for statistics and leaderboard business logic."""

from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.puzzle import Puzzle
from app.models.solve import Solve
from app.services.friend_service import FriendService
from app.services.puzzle_service import PuzzleService


class StatsService:
    """Service class for statistics and leaderboard operations."""

    def __init__(self, db: Session):
        self.db = db
        self.friend_service = FriendService(db)
        self.puzzle_service = PuzzleService(db)

    def get_solve(self, user_id: int, puzzle_id: int) -> Optional[Solve]:
        """Get a user's solve for a specific puzzle."""
        return (
            self.db.query(Solve)
            .filter(Solve.user_id == user_id, Solve.puzzle_id == puzzle_id)
            .first()
        )

    def submit_solve(
        self,
        user_id: int,
        puzzle_id: int,
        time_ms: int,
        user_grid: list[list[str]],
    ) -> tuple[Solve, bool, int]:
        """Submit a puzzle solve.

        Returns:
            tuple: (solve, is_new_record, rank)
        """
        # Get the puzzle
        puzzle = self.puzzle_service.get_by_id(puzzle_id)
        if not puzzle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Puzzle not found",
            )

        # Verify solution
        is_correct, _ = self.puzzle_service.check_solution(puzzle, user_grid)
        if not is_correct:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solution is incorrect",
            )

        # Check for existing solve
        existing_solve = self.get_solve(user_id, puzzle_id)
        is_new_record = False

        if existing_solve:
            # Update if new time is better
            if time_ms < existing_solve.time_ms:
                existing_solve.time_ms = time_ms
                is_new_record = True
            existing_solve.attempt_count += 1
            solve = existing_solve
        else:
            # Create new solve
            solve = Solve(
                user_id=user_id,
                puzzle_id=puzzle_id,
                time_ms=time_ms,
                is_completed=True,
            )
            self.db.add(solve)
            is_new_record = True

        self.db.commit()
        self.db.refresh(solve)

        # Get rank
        rank = self.get_user_rank(user_id, puzzle_id)

        return solve, is_new_record, rank

    def get_user_rank(self, user_id: int, puzzle_id: int) -> int:
        """Get user's rank on a puzzle leaderboard."""
        user_solve = self.get_solve(user_id, puzzle_id)
        if not user_solve:
            return 0

        # Count how many users have a better time
        better_count = (
            self.db.query(Solve)
            .filter(
                Solve.puzzle_id == puzzle_id,
                Solve.time_ms < user_solve.time_ms,
            )
            .count()
        )

        return better_count + 1

    def get_puzzle_leaderboard(
        self,
        puzzle_id: int,
        limit: int = 50,
        current_user_id: Optional[int] = None,
    ) -> list[dict]:
        """Get leaderboard for a puzzle."""
        solves = (
            self.db.query(Solve, User)
            .join(User, Solve.user_id == User.id)
            .filter(Solve.puzzle_id == puzzle_id, Solve.is_completed == True)
            .order_by(Solve.time_ms.asc())
            .limit(limit)
            .all()
        )

        # Get friend IDs if current user is logged in
        friend_ids = set()
        if current_user_id:
            friends = self.friend_service.get_friends(current_user_id)
            friend_ids = {f.id for f in friends}

        leaderboard = []
        for rank, (solve, user) in enumerate(solves, 1):
            leaderboard.append({
                "rank": rank,
                "user_id": user.id,
                "username": user.username,
                "time_ms": solve.time_ms,
                "completed_at": solve.completed_at,
                "is_friend": user.id in friend_ids,
                "is_current_user": user.id == current_user_id,
            })

        return leaderboard

    def get_friends_leaderboard(
        self,
        user_id: int,
        puzzle_id: int,
    ) -> list[dict]:
        """Get friends leaderboard for a puzzle (including the user)."""
        friends = self.friend_service.get_friends(user_id)
        friend_ids = [f.id for f in friends] + [user_id]

        solves = (
            self.db.query(Solve, User)
            .join(User, Solve.user_id == User.id)
            .filter(
                Solve.puzzle_id == puzzle_id,
                Solve.user_id.in_(friend_ids),
                Solve.is_completed == True,
            )
            .order_by(Solve.time_ms.asc())
            .all()
        )

        leaderboard = []
        for rank, (solve, user) in enumerate(solves, 1):
            leaderboard.append({
                "rank": rank,
                "user_id": user.id,
                "username": user.username,
                "time_ms": solve.time_ms,
                "completed_at": solve.completed_at,
                "is_friend": user.id != user_id,
                "is_current_user": user.id == user_id,
            })

        return leaderboard

    def get_user_stats(self, user_id: int) -> dict:
        """Get overall statistics for a user."""
        solves = self.db.query(Solve).filter(Solve.user_id == user_id).all()

        if not solves:
            return {
                "total_solves": 0,
                "average_time_ms": None,
                "best_time_ms": None,
                "total_time_ms": 0,
            }

        times = [s.time_ms for s in solves]
        return {
            "total_solves": len(solves),
            "average_time_ms": int(sum(times) / len(times)),
            "best_time_ms": min(times),
            "total_time_ms": sum(times),
        }

    def get_friends_count(self, user_id: int) -> int:
        """Get the number of friends a user has."""
        return len(self.friend_service.get_friends(user_id))

    def generate_share_text(
        self,
        puzzle: Puzzle,
        time_ms: int,
        puzzle_date: Optional[date] = None,
    ) -> str:
        """Generate a shareable result string (Wordle-style)."""
        minutes = time_ms // 60000
        seconds = (time_ms % 60000) // 1000

        date_str = puzzle_date.strftime("%Y-%m-%d") if puzzle_date else "Today"

        share_text = f"Daily Mini Crossword {date_str}\n"
        share_text += f"{puzzle.size}x{puzzle.size} - {puzzle.difficulty.capitalize()}\n"
        share_text += f"Time: {minutes}:{seconds:02d}\n"
        share_text += "\n"

        # Generate block pattern based on grid
        import json
        grid = json.loads(puzzle.grid)
        for row in grid:
            for cell in row:
                if cell == ".":
                    share_text += "⬛"
                else:
                    share_text += "🟩"
            share_text += "\n"

        share_text += "\nPlay at: [your-domain]/play"

        return share_text
