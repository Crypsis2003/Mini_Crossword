"""Cache metadata and dictionary models for puzzle generation."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Index

from app.database import Base


class DictionaryWord(Base):
    """Word dictionary for crossword generation."""

    __tablename__ = "dictionary_words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), nullable=False, unique=True)
    length = Column(Integer, nullable=False, index=True)
    frequency = Column(Integer, default=0)  # Optional ranking/frequency score
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_dictionary_words_length_word", "length", "word"),
    )


class PuzzleCacheMeta(Base):
    """Metadata for puzzle cache generation with concurrency control."""

    __tablename__ = "puzzle_cache_meta"

    id = Column(Integer, primary_key=True, index=True)
    week_key = Column(String(10), nullable=False, unique=True, index=True)
    status = Column(String(20), default="idle")  # idle, running, done, failed
    puzzle_count = Column(Integer, default=0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(String(500), nullable=True)
