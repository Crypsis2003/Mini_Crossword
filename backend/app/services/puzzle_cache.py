"""Puzzle cache management - generates and refreshes weekly puzzle pool."""

import json
import logging
import urllib.request
from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.puzzle import Puzzle
from app.models.cache_meta import PuzzleCacheMeta, DictionaryWord

logger = logging.getLogger(__name__)

# Constants
PUZZLE_COUNT = 25
GENERATION_TIMEOUT_MINUTES = 10
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 7

# Public word list URL (MIT licensed)
WORD_LIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"


def get_current_week_key() -> str:
    """Get current ISO week key (e.g., '2026-W02')."""
    today = date.today()
    return today.strftime("%G-W%V")


def ensure_dictionary(db: Session) -> None:
    """
    Ensure dictionary is loaded in DB. Downloads if missing.
    """
    count = db.query(DictionaryWord).count()
    if count > 0:
        logger.debug(f"Dictionary already loaded: {count} words")
        return

    logger.info("Dictionary not found, downloading...")
    _download_and_store_dictionary(db)


def _download_and_store_dictionary(db: Session) -> int:
    """Download word list and store in database."""
    try:
        # Download word list
        logger.info(f"Downloading word list from {WORD_LIST_URL}")
        with urllib.request.urlopen(WORD_LIST_URL, timeout=30) as response:
            content = response.read().decode("utf-8")

        # Parse and filter words
        words = []
        for line in content.splitlines():
            word = line.strip().upper()
            if (
                word
                and word.isalpha()
                and MIN_WORD_LENGTH <= len(word) <= MAX_WORD_LENGTH
            ):
                words.append(word)

        # Remove duplicates and sort
        words = sorted(set(words))
        logger.info(f"Filtered to {len(words)} words ({MIN_WORD_LENGTH}-{MAX_WORD_LENGTH} letters)")

        # Batch insert
        batch_size = 1000
        for i in range(0, len(words), batch_size):
            batch = words[i : i + batch_size]
            for word in batch:
                db.add(DictionaryWord(word=word, length=len(word)))
            db.flush()

        db.commit()
        logger.info(f"Successfully stored {len(words)} words in dictionary")
        return len(words)

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to download dictionary: {e}")
        raise


def get_words_by_length(db: Session, length: int) -> list[str]:
    """Get all words of a specific length from dictionary."""
    words = db.query(DictionaryWord.word).filter(
        DictionaryWord.length == length
    ).all()
    return [w[0] for w in words]


def ensure_weekly_cache(db: Session) -> None:
    """
    Ensure puzzle cache exists for current week.

    Concurrency-safe: uses PuzzleCacheMeta to prevent duplicate generation.
    Called automatically on puzzle requests.
    """
    week_key = get_current_week_key()

    # First, ensure dictionary is available
    ensure_dictionary(db)

    # Check if cache meta exists for this week
    meta = db.query(PuzzleCacheMeta).filter(
        PuzzleCacheMeta.week_key == week_key
    ).first()

    if meta:
        if meta.status == "done" and meta.puzzle_count >= PUZZLE_COUNT:
            # Cache is ready
            return

        if meta.status == "running":
            # Check for stale lock (generation taking too long)
            if meta.started_at:
                elapsed = (datetime.utcnow() - meta.started_at).total_seconds()
                if elapsed < GENERATION_TIMEOUT_MINUTES * 60:
                    logger.info(f"Generation already in progress for {week_key}")
                    return
                else:
                    logger.warning(f"Stale generation lock detected for {week_key}, resetting")
                    meta.status = "idle"
                    db.commit()

    # Try to acquire generation lock
    if not _acquire_generation_lock(db, week_key):
        logger.info(f"Could not acquire lock for {week_key}, another process is generating")
        return

    try:
        _refresh_weekly_cache(db, week_key)
    except Exception as e:
        logger.error(f"Generation failed for {week_key}: {e}")
        _mark_generation_failed(db, week_key, str(e))
        raise


def _acquire_generation_lock(db: Session, week_key: str) -> bool:
    """Try to acquire generation lock. Returns True if acquired."""
    try:
        # Try to insert new meta row (atomic)
        meta = PuzzleCacheMeta(
            week_key=week_key,
            status="running",
            started_at=datetime.utcnow(),
        )
        db.add(meta)
        db.commit()
        logger.info(f"Acquired generation lock for {week_key}")
        return True
    except IntegrityError:
        db.rollback()
        # Row exists, try to update if idle/failed
        meta = db.query(PuzzleCacheMeta).filter(
            PuzzleCacheMeta.week_key == week_key,
            PuzzleCacheMeta.status.in_(["idle", "failed"])
        ).first()

        if meta:
            meta.status = "running"
            meta.started_at = datetime.utcnow()
            meta.error_message = None
            db.commit()
            logger.info(f"Re-acquired generation lock for {week_key}")
            return True

        return False


def _mark_generation_failed(db: Session, week_key: str, error: str) -> None:
    """Mark generation as failed."""
    meta = db.query(PuzzleCacheMeta).filter(
        PuzzleCacheMeta.week_key == week_key
    ).first()
    if meta:
        meta.status = "failed"
        meta.error_message = error[:500]
        db.commit()


def _refresh_weekly_cache(db: Session, week_key: str) -> int:
    """
    Generate and store puzzles for the week.

    Returns number of puzzles created.
    """
    logger.info(f"Generating {PUZZLE_COUNT} puzzles for {week_key}...")

    # Delete any existing puzzles for this week (idempotent)
    deleted = db.query(Puzzle).filter(Puzzle.week_key == week_key).delete()
    if deleted:
        logger.info(f"Deleted {deleted} existing puzzles for {week_key}")

    # Generate new puzzles
    puzzles = generate_puzzle_set(db, n=PUZZLE_COUNT)

    # Insert into database
    for i, puzzle_data in enumerate(puzzles):
        puzzle = Puzzle(
            title=puzzle_data["title"],
            size=puzzle_data["size"],
            difficulty=puzzle_data["difficulty"],
            grid=json.dumps(puzzle_data["grid"]),
            solution=json.dumps(puzzle_data["solution"]),
            clues_across=json.dumps(puzzle_data["clues_across"]),
            clues_down=json.dumps(puzzle_data["clues_down"]),
            week_key=week_key,
            scheduled_date=None,
        )
        db.add(puzzle)

    # Update meta
    meta = db.query(PuzzleCacheMeta).filter(
        PuzzleCacheMeta.week_key == week_key
    ).first()
    if meta:
        meta.status = "done"
        meta.puzzle_count = len(puzzles)
        meta.completed_at = datetime.utcnow()

    db.commit()
    logger.info(f"Successfully created {len(puzzles)} puzzles for {week_key}")
    return len(puzzles)


def generate_puzzle_set(db: Session, n: int = 25) -> list[dict]:
    """
    Generate n valid crossword puzzles using the real generator.
    """
    import random
    from app.services.crossword_generator import generate_puzzle

    # Load words from database, grouped by length
    words_by_length: dict[int, list[str]] = {}
    for length in range(MIN_WORD_LENGTH, MAX_WORD_LENGTH + 1):
        words = get_words_by_length(db, length)
        if words:
            words_by_length[length] = words
            logger.debug(f"Loaded {len(words)} words of length {length}")

    if not words_by_length:
        logger.error("No words in dictionary, cannot generate puzzles")
        return []

    puzzles = []
    failed_count = 0
    max_failures = n * 2  # Allow some failures

    i = 0
    while len(puzzles) < n and failed_count < max_failures:
        size = random.choice([5, 6, 7])

        puzzle_data = generate_puzzle(size, words_by_length, max_attempts=30)
        if puzzle_data:
            # Add metadata
            puzzle_data["title"] = f"Puzzle {i + 1}"
            puzzle_data["difficulty"] = _estimate_difficulty(puzzle_data)
            puzzles.append(puzzle_data)
            logger.info(f"Generated puzzle {len(puzzles)}/{n} (size={size})")
            i += 1
        else:
            failed_count += 1
            logger.warning(f"Failed to generate puzzle (attempt {failed_count})")

    if len(puzzles) < n:
        logger.error(f"Only generated {len(puzzles)}/{n} puzzles")

    return puzzles


def _estimate_difficulty(puzzle: dict) -> str:
    """Estimate puzzle difficulty based on size and word count."""
    size = puzzle["size"]
    num_clues = len(puzzle["clues_across"]) + len(puzzle["clues_down"])

    if size <= 5 and num_clues <= 8:
        return "easy"
    elif size >= 7 or num_clues >= 14:
        return "hard"
    else:
        return "medium"
