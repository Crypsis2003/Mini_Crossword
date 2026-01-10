"""Solve model for tracking user puzzle completions."""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Solve(Base):
    """User puzzle solve record."""

    __tablename__ = "solves"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    puzzle_id = Column(Integer, ForeignKey("puzzles.id", ondelete="CASCADE"), nullable=False, index=True)
    time_ms = Column(Integer, nullable=False)  # Solve time in milliseconds
    completed_at = Column(DateTime, default=datetime.utcnow)
    is_completed = Column(Boolean, default=True)
    attempt_count = Column(Integer, default=1)
    hints_used = Column(Integer, default=0)  # Number of hints used

    # Relationships
    user = relationship("User", back_populates="solves")
    puzzle = relationship("Puzzle", back_populates="solves")

    # Ensure one solve record per user per puzzle
    __table_args__ = (
        UniqueConstraint("user_id", "puzzle_id", name="unique_user_puzzle_solve"),
    )

    def __repr__(self):
        return f"<Solve(user_id={self.user_id}, puzzle_id={self.puzzle_id}, time_ms={self.time_ms}, hints_used={self.hints_used})>"
