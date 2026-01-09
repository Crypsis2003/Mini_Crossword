"""Puzzle model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Puzzle(Base):
    """Crossword puzzle model."""

    __tablename__ = "puzzles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)  # Grid size (5, 6, or 7)
    grid = Column(Text, nullable=False)  # JSON string of grid layout (with blocks marked)
    solution = Column(Text, nullable=False)  # JSON string of solution
    clues_across = Column(Text, nullable=False)  # JSON string of across clues
    clues_down = Column(Text, nullable=False)  # JSON string of down clues
    scheduled_date = Column(Date, unique=True, index=True, nullable=True)  # Date when this puzzle is active
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    week_key = Column(String(10), index=True, nullable=True)  # ISO week like "2026-W02" for cache tracking
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    solves = relationship("Solve", back_populates="puzzle", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Puzzle(id={self.id}, title={self.title}, size={self.size}x{self.size})>"
