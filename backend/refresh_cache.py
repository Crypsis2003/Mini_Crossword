#!/usr/bin/env python3
"""CLI script to manually refresh the puzzle cache."""

import argparse
import logging
import sys

sys.path.insert(0, ".")

from app.database import SessionLocal, init_db
from app.services.puzzle_cache import (
    get_current_week_key,
    is_cache_current,
    refresh_cache,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Refresh puzzle cache")
    parser.add_argument(
        "--week",
        type=str,
        default=None,
        help="Week key (e.g., 2026-W02). Defaults to current week.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force refresh even if cache exists",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check if cache is current (no refresh)",
    )
    args = parser.parse_args()

    # Initialize DB
    init_db()
    db = SessionLocal()

    try:
        week_key = args.week or get_current_week_key()
        print(f"Week key: {week_key}")

        if args.check:
            current = is_cache_current(db, week_key)
            print(f"Cache current: {current}")
            sys.exit(0 if current else 1)

        count = refresh_cache(db, week_key, force=args.force)
        if count > 0:
            print(f"Created {count} puzzles for {week_key}")
        else:
            print(f"Cache already current for {week_key} (use --force to regenerate)")

    finally:
        db.close()


if __name__ == "__main__":
    main()
