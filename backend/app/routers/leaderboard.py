"""Public leaderboard router - no auth required."""

import logging
import re
import hashlib
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.leaderboard_entry import DailyLeaderboardEntry
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

# Constants
MAX_NAME_LENGTH = 30
MIN_TIME_MS = 1000  # 1 second minimum (anti-cheat)
MAX_TIME_MS = 3600000  # 1 hour maximum


class LeaderboardSubmit(BaseModel):
    """Request body for submitting a leaderboard entry."""
    name: str = Field(default="Anonymous", max_length=MAX_NAME_LENGTH)
    time_ms: int = Field(..., ge=MIN_TIME_MS, le=MAX_TIME_MS)
    puzzle_date: str = Field(default=None)  # Optional, defaults to today

    @validator('name', pre=True, always=True)
    def sanitize_name(cls, v):
        if not v:
            return "Anonymous"
        # Strip whitespace
        v = str(v).strip()
        # Only allow letters, numbers, spaces, and basic punctuation
        v = re.sub(r'[^a-zA-Z0-9 ._-]', '', v)
        # Collapse multiple spaces
        v = re.sub(r'\s+', ' ', v).strip()
        if not v:
            return "Anonymous"
        return v[:MAX_NAME_LENGTH]


def hash_ip(ip: str) -> str:
    """Hash IP address for abuse tracking (don't store raw IPs)."""
    secret = settings.secret_key or "default-secret"
    return hashlib.sha256(f"{ip}:{secret}".encode()).hexdigest()[:16]


@router.get("/today")
def get_today_leaderboard(db: Session = Depends(get_db)):
    """
    Get public leaderboard for today's puzzle.
    Returns sorted entries (fastest first) with ranks.
    """
    today = date.today()

    entries = db.query(DailyLeaderboardEntry).filter(
        DailyLeaderboardEntry.puzzle_date == today
    ).order_by(DailyLeaderboardEntry.time_ms).limit(100).all()

    return {
        "puzzle_date": today.isoformat(),
        "entries": [
            {
                "rank": i + 1,
                "name": entry.name,
                "time_ms": entry.time_ms,
                "created_at": entry.created_at.isoformat() if entry.created_at else None,
            }
            for i, entry in enumerate(entries)
        ],
        "total_count": len(entries),
    }


@router.post("/submit")
def submit_leaderboard_entry(
    data: LeaderboardSubmit,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Submit a solve time to the public leaderboard.
    Called after puzzle completion with user-entered name.
    """
    # Determine puzzle date (default to today)
    if data.puzzle_date:
        try:
            puzzle_date = date.fromisoformat(data.puzzle_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid puzzle_date format")
    else:
        puzzle_date = date.today()

    # Don't allow submissions for future dates
    if puzzle_date > date.today():
        raise HTTPException(status_code=400, detail="Cannot submit for future dates")

    # Get client IP for abuse tracking (hashed)
    client_ip = request.client.host if request.client else "unknown"
    ip_hash = hash_ip(client_ip)

    # Optional: Rate limit by IP (max 5 submissions per day per IP)
    existing_count = db.query(DailyLeaderboardEntry).filter(
        DailyLeaderboardEntry.puzzle_date == puzzle_date,
        DailyLeaderboardEntry.ip_hash == ip_hash,
    ).count()

    if existing_count >= 5:
        raise HTTPException(
            status_code=429,
            detail="Too many submissions. Max 5 per day."
        )

    # Create entry
    entry = DailyLeaderboardEntry(
        puzzle_date=puzzle_date,
        name=data.name,
        time_ms=data.time_ms,
        ip_hash=ip_hash,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    # Calculate rank
    rank = db.query(DailyLeaderboardEntry).filter(
        DailyLeaderboardEntry.puzzle_date == puzzle_date,
        DailyLeaderboardEntry.time_ms < entry.time_ms,
    ).count() + 1

    logger.info(f"Leaderboard entry: {data.name} - {data.time_ms}ms (rank #{rank})")

    return {
        "success": True,
        "rank": rank,
        "name": entry.name,
        "time_ms": entry.time_ms,
        "puzzle_date": puzzle_date.isoformat(),
    }
