#!/usr/bin/env python3
"""
Weekly puzzle refresh script.

This script regenerates puzzles for the current week using real clues
from the public domain clue database.

Usage:
    # Manual refresh
    python scripts/refresh_puzzles.py

    # Force refresh (delete existing puzzles first)
    python scripts/refresh_puzzles.py --force

    # On Render, you can set up a Cron Job to run this weekly
    # Cron expression for Monday at 00:00 UTC: 0 0 * * 1
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, init_db
from app.services.puzzle_cache import (
    ensure_weekly_cache,
    get_current_week_key,
    PUZZLE_COUNT,
)
from app.models.puzzle import Puzzle
from app.models.cache_meta import PuzzleCacheMeta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def refresh_puzzles(force: bool = False) -> dict:
    """
    Refresh puzzles for the current week.

    Args:
        force: If True, delete existing puzzles and regenerate

    Returns:
        dict with results
    """
    init_db()
    db = SessionLocal()

    try:
        week_key = get_current_week_key()
        logger.info(f"Refreshing puzzles for week: {week_key}")

        if force:
            # Delete existing puzzles and cache meta for this week
            deleted_puzzles = db.query(Puzzle).filter(
                Puzzle.week_key == week_key
            ).delete()
            deleted_meta = db.query(PuzzleCacheMeta).filter(
                PuzzleCacheMeta.week_key == week_key
            ).delete()
            db.commit()
            logger.info(f"Force refresh: deleted {deleted_puzzles} puzzles, {deleted_meta} meta entries")

        # Ensure cache is populated (this will generate if missing)
        ensure_weekly_cache(db)

        # Get the generated puzzles
        puzzles = db.query(Puzzle).filter(
            Puzzle.week_key == week_key
        ).order_by(Puzzle.scheduled_date).all()

        result = {
            "success": True,
            "week_key": week_key,
            "puzzle_count": len(puzzles),
            "puzzles": [
                {
                    "id": p.id,
                    "title": p.title,
                    "scheduled_date": str(p.scheduled_date) if p.scheduled_date else None,
                }
                for p in puzzles
            ],
        }

        logger.info(f"Successfully refreshed {len(puzzles)} puzzles for {week_key}")
        return result

    except Exception as e:
        logger.error(f"Error refreshing puzzles: {e}")
        return {
            "success": False,
            "error": str(e),
            "week_key": get_current_week_key(),
        }

    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Refresh weekly crossword puzzles with real clues"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force refresh - delete existing puzzles and regenerate",
    )
    args = parser.parse_args()

    result = refresh_puzzles(force=args.force)

    if result["success"]:
        print(f"\nSuccess! Generated {result['puzzle_count']} puzzles for {result['week_key']}")
        print("\nPuzzles:")
        for p in result["puzzles"]:
            print(f"  - {p['scheduled_date']}: {p['title']} (ID: {p['id']})")
    else:
        print(f"\nError: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
