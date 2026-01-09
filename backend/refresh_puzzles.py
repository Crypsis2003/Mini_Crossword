#!/usr/bin/env python3
"""Manually refresh puzzles for the current week."""

import sys
sys.path.insert(0, ".")

from app.database import SessionLocal, init_db
from app.models.puzzle import Puzzle
from app.models.cache_meta import PuzzleCacheMeta
from app.services.puzzle_cache import get_current_week_key, ensure_weekly_cache

init_db()
db = SessionLocal()

week_key = get_current_week_key()
print(f"Current week: {week_key}")

# Delete existing puzzles and cache meta for this week
deleted_puzzles = db.query(Puzzle).filter(Puzzle.week_key == week_key).delete()
deleted_meta = db.query(PuzzleCacheMeta).filter(PuzzleCacheMeta.week_key == week_key).delete()
db.commit()

print(f"Deleted {deleted_puzzles} puzzles and {deleted_meta} cache entries")

# Regenerate
print("Regenerating puzzles...")
ensure_weekly_cache(db)

# Show results
puzzles = db.query(Puzzle).filter(Puzzle.week_key == week_key).order_by(Puzzle.scheduled_date).all()
print(f"\nGenerated {len(puzzles)} puzzles:")
for p in puzzles:
    print(f"  {p.scheduled_date}: {p.title} ({p.size}x{p.size})")

db.close()
print("\nDone!")
