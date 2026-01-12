"""Daily leaderboard entry model - public, no auth required."""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Date, Index

from app.database import Base


class DailyLeaderboardEntry(Base):
    """Public leaderboard entry for daily puzzles."""

    __tablename__ = "daily_leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    puzzle_date = Column(Date, nullable=False, index=True)
    name = Column(String(30), nullable=False)  # Display name, sanitized
    time_ms = Column(Integer, nullable=False)  # Solve time in milliseconds
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_hash = Column(String(64), nullable=True)  # Optional: hashed IP for abuse control

    __table_args__ = (
        Index('ix_leaderboard_date_time', 'puzzle_date', 'time_ms'),
    )
