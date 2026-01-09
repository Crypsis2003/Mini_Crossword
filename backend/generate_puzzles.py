#!/usr/bin/env python3
"""CLI to pre-generate puzzle cache."""

import logging
import sys

sys.path.insert(0, ".")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

from app.database import SessionLocal, init_db
from app.services.puzzle_cache import (
    ensure_dictionary,
    ensure_weekly_cache,
    get_current_week_key,
)

def main():
    print("Initializing database...")
    init_db()

    db = SessionLocal()
    try:
        week_key = get_current_week_key()
        print(f"Generating puzzles for week: {week_key}")

        print("Step 1: Ensuring dictionary is loaded...")
        ensure_dictionary(db)

        print("Step 2: Generating weekly puzzle cache...")
        ensure_weekly_cache(db)

        print("Done! Puzzles are ready.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
