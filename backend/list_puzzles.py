#!/usr/bin/env python3
"""List all puzzles in the database."""

import sys
sys.path.insert(0, ".")

from app.database import SessionLocal, init_db
from app.models.puzzle import Puzzle

init_db()
db = SessionLocal()

puzzles = db.query(Puzzle).order_by(Puzzle.scheduled_date).all()

print(f"\n{'='*60}")
print(f"Total puzzles: {len(puzzles)}")
print(f"{'='*60}\n")

for p in puzzles:
    print(f"ID: {p.id}")
    print(f"  Title: {p.title}")
    print(f"  Size: {p.size}x{p.size}")
    print(f"  Difficulty: {p.difficulty}")
    print(f"  Scheduled: {p.scheduled_date}")
    print(f"  Week Key: {p.week_key}")
    print()

db.close()
