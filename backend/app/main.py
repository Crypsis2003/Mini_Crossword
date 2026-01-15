"""Main FastAPI application."""

import logging
import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from app.config import get_settings
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Determine paths - works both locally and on Render
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# Log the paths for debugging
logger.info(f"APP_DIR: {APP_DIR}")
logger.info(f"BACKEND_DIR: {BACKEND_DIR}")
logger.info(f"PROJECT_ROOT: {PROJECT_ROOT}")
logger.info(f"FRONTEND_DIR: {FRONTEND_DIR}")
logger.info(f"FRONTEND_DIR exists: {FRONTEND_DIR.exists()}")

if FRONTEND_DIR.exists():
    logger.info(f"Frontend contents: {list(FRONTEND_DIR.iterdir())}")


def run_migrations():
    """Run any pending database migrations."""
    from app.database import engine
    from sqlalchemy import text

    migrations = [
        # Add week_key column to puzzles table
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'puzzles' AND column_name = 'week_key'
            ) THEN
                ALTER TABLE puzzles ADD COLUMN week_key VARCHAR(10);
                CREATE INDEX IF NOT EXISTS ix_puzzles_week_key ON puzzles(week_key);
            END IF;
        END $$;
        """,
        # Create dictionary_words table if not exists
        """
        CREATE TABLE IF NOT EXISTS dictionary_words (
            id SERIAL PRIMARY KEY,
            word VARCHAR(50) NOT NULL UNIQUE,
            length INTEGER NOT NULL,
            frequency INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS ix_dictionary_words_length ON dictionary_words(length);
        CREATE INDEX IF NOT EXISTS ix_dictionary_words_length_word ON dictionary_words(length, word);
        """,
        # Create puzzle_cache_meta table if not exists
        """
        CREATE TABLE IF NOT EXISTS puzzle_cache_meta (
            id SERIAL PRIMARY KEY,
            week_key VARCHAR(10) NOT NULL UNIQUE,
            status VARCHAR(20) DEFAULT 'idle',
            puzzle_count INTEGER DEFAULT 0,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message VARCHAR(500)
        );
        CREATE INDEX IF NOT EXISTS ix_puzzle_cache_meta_week_key ON puzzle_cache_meta(week_key);
        """,
        # Create daily_leaderboard_entries table for public leaderboard
        """
        CREATE TABLE IF NOT EXISTS daily_leaderboard_entries (
            id SERIAL PRIMARY KEY,
            puzzle_date DATE NOT NULL,
            name VARCHAR(30) NOT NULL,
            time_ms INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_hash VARCHAR(64)
        );
        CREATE INDEX IF NOT EXISTS ix_leaderboard_date ON daily_leaderboard_entries(puzzle_date);
        CREATE INDEX IF NOT EXISTS ix_leaderboard_date_time ON daily_leaderboard_entries(puzzle_date, time_ms);
        """
    ]

    with engine.connect() as conn:
        for migration in migrations:
            try:
                conn.execute(text(migration))
                conn.commit()
            except Exception as e:
                logger.warning(f"Migration warning (may be OK): {e}")
                conn.rollback()

    logger.info("Database migrations completed")


def ensure_puzzles_ready():
    """Ensure puzzle cache is populated (runs in background thread)."""
    import threading
    import time

    def _generate():
        from app.database import SessionLocal
        from app.services.puzzle_cache import ensure_weekly_cache, get_current_week_key
        from app.models.puzzle import Puzzle
        from app.models.cache_meta import PuzzleCacheMeta

        # Wait a moment for app to fully start
        time.sleep(2)

        db = SessionLocal()
        try:
            week_key = get_current_week_key()

            # One-time migration: Clear old puzzles that don't have real clues
            old_puzzle = db.query(Puzzle).filter(
                Puzzle.clues_across.like('%Garden bloom%')
            ).first()

            if old_puzzle:
                logger.info("Detected old puzzles with generic clues - clearing...")
                db.query(Puzzle).delete()
                db.query(PuzzleCacheMeta).delete()
                db.commit()
                logger.info("Cleared old puzzle data")

            # Check if puzzles already exist
            existing = db.query(Puzzle).filter(Puzzle.week_key == week_key).count()
            if existing >= 7:
                logger.info(f"Puzzles already exist for {week_key} ({existing} puzzles)")
                return

            logger.info(f"Background: Generating puzzles for {week_key}...")
            ensure_weekly_cache(db)
            logger.info("Background: Puzzle cache ready!")
        except Exception as e:
            logger.error(f"Background: Error generating puzzles: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()

    # Run in background thread (NOT daemon, so it completes even if main thread is idle)
    thread = threading.Thread(target=_generate, daemon=False)
    thread.start()
    logger.info("Started background puzzle generation thread")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting application...")
    init_db()
    logger.info("Database initialized")
    run_migrations()
    ensure_puzzles_ready()
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.app_name,
    description="A daily mini crossword puzzle game",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routers FIRST
from app.routers import auth_router, puzzles_router, friends_router, leaderboard_router

app.include_router(auth_router, prefix="/api")
app.include_router(puzzles_router, prefix="/api")
app.include_router(friends_router, prefix="/api")
app.include_router(leaderboard_router, prefix="/api")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.app_name}


# Serve index.html for root
@app.get("/", response_class=HTMLResponse)
@app.head("/")
async def serve_index():
    """Serve the main frontend page."""
    index_path = FRONTEND_DIR / "index.html"
    logger.info(f"Serving index from: {index_path}, exists: {index_path.exists()}")
    if index_path.exists():
        return FileResponse(str(index_path), media_type="text/html")
    return HTMLResponse(content="<h1>Daily Mini Crossword API</h1><p>Frontend not found. API docs at <a href='/docs'>/docs</a></p>", status_code=200)


# Serve static files (CSS, JS)
if FRONTEND_DIR.exists():
    # Mount CSS directory
    css_dir = FRONTEND_DIR / "css"
    if css_dir.exists():
        app.mount("/static/css", StaticFiles(directory=str(css_dir)), name="css")
        logger.info(f"Mounted CSS from {css_dir}")

    # Mount JS directory
    js_dir = FRONTEND_DIR / "js"
    if js_dir.exists():
        app.mount("/static/js", StaticFiles(directory=str(js_dir)), name="js")
        logger.info(f"Mounted JS from {js_dir}")

    # Also mount the whole frontend directory for any other static files
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    logger.info(f"Mounted static files from {FRONTEND_DIR}")
else:
    logger.warning(f"Frontend directory not found at {FRONTEND_DIR}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", settings.port))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
    )
