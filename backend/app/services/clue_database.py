"""Clue database service - provides real crossword clues from public domain sources."""

import os
import random
import logging
from pathlib import Path
from functools import lru_cache
from collections import defaultdict
from typing import Optional

logger = logging.getLogger(__name__)

# Path to clues file
DATA_DIR = Path(__file__).parent.parent.parent / "data"
CLUES_FILE = DATA_DIR / "clues.tsv"


class ClueDatabase:
    """Database of crossword clues indexed by answer word."""

    _instance: Optional["ClueDatabase"] = None

    def __init__(self):
        self.clues: dict[str, list[str]] = defaultdict(list)
        self.loaded = False

    @classmethod
    def get_instance(cls) -> "ClueDatabase":
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = ClueDatabase()
        return cls._instance

    def load(self) -> bool:
        """Load clues from TSV file. Returns True if successful."""
        if self.loaded:
            return True

        if not CLUES_FILE.exists():
            logger.warning(f"Clues file not found: {CLUES_FILE}")
            return False

        logger.info(f"Loading clues from {CLUES_FILE}...")

        try:
            count = 0
            with open(CLUES_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                # Skip header
                next(f, None)

                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 4:
                        # Format: pubid, year, answer, clue
                        answer = parts[2].upper().strip()
                        clue = parts[3].strip()

                        # Only keep words 3-5 letters (for mini crosswords)
                        # and valid clues
                        if 3 <= len(answer) <= 5 and clue and answer.isalpha():
                            self.clues[answer].append(clue)
                            count += 1

            self.loaded = True
            logger.info(f"Loaded {count} clues for {len(self.clues)} unique words")
            return True

        except Exception as e:
            logger.error(f"Error loading clues: {e}")
            return False

    def get_clue(self, word: str) -> Optional[str]:
        """Get a random clue for a word."""
        if not self.loaded:
            self.load()

        word = word.upper().strip()
        clues = self.clues.get(word, [])

        if clues:
            return random.choice(clues)
        return None

    def get_all_clues(self, word: str) -> list[str]:
        """Get all clues for a word."""
        if not self.loaded:
            self.load()

        word = word.upper().strip()
        return self.clues.get(word, [])

    def has_clue(self, word: str) -> bool:
        """Check if we have a clue for this word."""
        if not self.loaded:
            self.load()

        word = word.upper().strip()
        return word in self.clues

    def get_words_with_clues(self, length: int) -> list[str]:
        """Get all words of a specific length that have clues."""
        if not self.loaded:
            self.load()

        return [word for word in self.clues.keys() if len(word) == length]

    def stats(self) -> dict:
        """Get statistics about the clue database."""
        if not self.loaded:
            self.load()

        by_length = defaultdict(int)
        for word in self.clues.keys():
            by_length[len(word)] += 1

        return {
            "total_words": len(self.clues),
            "total_clues": sum(len(c) for c in self.clues.values()),
            "by_length": dict(by_length),
        }


@lru_cache(maxsize=1)
def get_clue_database() -> ClueDatabase:
    """Get the clue database singleton."""
    db = ClueDatabase.get_instance()
    db.load()
    return db


def get_clue_for_word(word: str) -> Optional[str]:
    """Convenience function to get a clue for a word."""
    return get_clue_database().get_clue(word)


def generate_fallback_clue(word: str) -> str:
    """Generate a simple fallback clue if no real clue is available."""
    word = word.upper()

    # Simple pattern-based fallback clues
    if len(word) == 3:
        return f"Three-letter word"
    elif len(word) == 4:
        return f"Four-letter word starting with {word[0]}"
    elif len(word) == 5:
        return f"Five-letter word ending in {word[-1]}"
    else:
        return f"Word: {word[0]}{'_' * (len(word) - 2)}{word[-1]}"
