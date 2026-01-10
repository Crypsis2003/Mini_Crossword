#!/usr/bin/env python3
"""
Management script for Mini Crossword backend.

Usage:
    python manage.py generate     # Generate puzzles for current week
    python manage.py refresh      # Force refresh puzzles for current week
    python manage.py list         # List all puzzles in database
    python manage.py migrate      # Run database migrations
"""

import argparse
import logging
import sys

sys.path.insert(0, ".")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def cmd_generate(args):
    """Generate puzzles for the current week."""
    from app.database import SessionLocal, init_db
    from app.services.puzzle_cache import (
        ensure_dictionary,
        ensure_weekly_cache,
        get_current_week_key,
    )

    logger.info("Initializing database...")
    init_db()

    db = SessionLocal()
    try:
        week_key = get_current_week_key()
        logger.info(f"Generating puzzles for week: {week_key}")

        logger.info("Step 1: Ensuring dictionary is loaded...")
        ensure_dictionary(db)

        logger.info("Step 2: Generating weekly puzzle cache...")
        ensure_weekly_cache(db)

        logger.info("Done! Puzzles are ready.")
    finally:
        db.close()


def cmd_refresh(args):
    """Force refresh puzzles for the current week."""
    from app.database import SessionLocal, init_db
    from app.models.puzzle import Puzzle
    from app.models.cache_meta import PuzzleCacheMeta
    from app.services.puzzle_cache import (
        get_current_week_key,
        ensure_weekly_cache,
        ensure_dictionary,
    )

    logger.info("Initializing database...")
    init_db()

    db = SessionLocal()
    try:
        week_key = args.week or get_current_week_key()
        logger.info(f"Refreshing puzzles for week: {week_key}")

        # Ensure dictionary is loaded
        logger.info("Ensuring dictionary is loaded...")
        ensure_dictionary(db)

        # Delete existing puzzles and cache meta for this week
        deleted_puzzles = db.query(Puzzle).filter(Puzzle.week_key == week_key).delete()
        deleted_meta = db.query(PuzzleCacheMeta).filter(
            PuzzleCacheMeta.week_key == week_key
        ).delete()
        db.commit()

        logger.info(f"Deleted {deleted_puzzles} puzzles and {deleted_meta} cache entries")

        # Regenerate
        logger.info("Regenerating puzzles...")
        ensure_weekly_cache(db)

        # Show results
        puzzles = db.query(Puzzle).filter(
            Puzzle.week_key == week_key
        ).order_by(Puzzle.scheduled_date).all()

        logger.info(f"\nGenerated {len(puzzles)} puzzles:")
        for p in puzzles:
            # Show first across word as preview
            import json
            solution = json.loads(p.solution)
            first_word = "".join(solution[0]).replace("#", "")[:5]
            logger.info(f"  {p.scheduled_date}: {p.title} ({p.size}x{p.size}) - {first_word}...")

        logger.info("\nDone!")
    finally:
        db.close()


def cmd_list(args):
    """List all puzzles in the database."""
    from app.database import SessionLocal, init_db
    from app.models.puzzle import Puzzle
    import json

    init_db()
    db = SessionLocal()

    try:
        puzzles = db.query(Puzzle).order_by(Puzzle.scheduled_date).all()

        print(f"\n{'='*70}")
        print(f"Total puzzles: {len(puzzles)}")
        print(f"{'='*70}\n")

        for p in puzzles:
            print(f"ID: {p.id}")
            print(f"  Title: {p.title}")
            print(f"  Size: {p.size}x{p.size}")
            print(f"  Difficulty: {p.difficulty}")
            print(f"  Scheduled: {p.scheduled_date}")
            print(f"  Week Key: {p.week_key}")

            # Show solution preview
            solution = json.loads(p.solution)
            print(f"  Solution:")
            for row in solution:
                print(f"    {''.join(row)}")
            print()
    finally:
        db.close()


def cmd_migrate(args):
    """Run database migrations."""
    import subprocess
    result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


def cmd_test_generate(args):
    """Test puzzle generation without saving to database."""
    from app.database import SessionLocal, init_db
    from app.services.puzzle_templates import generate_validated_puzzle
    from app.services.puzzle_cache import ensure_dictionary

    logger.info("Initializing database...")
    init_db()

    db = SessionLocal()
    try:
        logger.info("Ensuring dictionary is loaded...")
        ensure_dictionary(db)

        logger.info("Generating test puzzle...")
        puzzle = generate_validated_puzzle(db)

        if puzzle:
            print(f"\nGenerated {puzzle['size']}x{puzzle['size']} puzzle:")
            print("\nSolution:")
            for row in puzzle['solution']:
                print(f"  {''.join(row)}")

            print("\nAcross clues:")
            for clue in puzzle['clues_across']:
                print(f"  {clue['number']}. {clue['clue']} ({clue['length']} letters)")

            print("\nDown clues:")
            for clue in puzzle['clues_down']:
                print(f"  {clue['number']}. {clue['clue']} ({clue['length']} letters)")
        else:
            logger.error("Failed to generate puzzle!")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Mini Crossword Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage.py generate          Generate puzzles for current week
  python manage.py refresh           Force refresh current week's puzzles
  python manage.py refresh --week 2026-W03   Refresh specific week
  python manage.py list              List all puzzles
  python manage.py migrate           Run database migrations
  python manage.py test              Test puzzle generation
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # generate command
    subparsers.add_parser("generate", help="Generate puzzles for current week")

    # refresh command
    refresh_parser = subparsers.add_parser("refresh", help="Force refresh puzzles")
    refresh_parser.add_argument(
        "--week",
        type=str,
        default=None,
        help="Week key (e.g., 2026-W02). Defaults to current week."
    )

    # list command
    subparsers.add_parser("list", help="List all puzzles")

    # migrate command
    subparsers.add_parser("migrate", help="Run database migrations")

    # test command
    subparsers.add_parser("test", help="Test puzzle generation")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "refresh":
        cmd_refresh(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "migrate":
        sys.exit(cmd_migrate(args))
    elif args.command == "test":
        cmd_test_generate(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
