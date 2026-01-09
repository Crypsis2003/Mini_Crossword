"""Main FastAPI application."""

import logging
import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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
# When running from backend/, frontend is at ../frontend
# When running from repo root, frontend is at ./frontend
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# Fallback if frontend is not found at expected location
if not FRONTEND_DIR.exists():
    # Try relative to current working directory
    FRONTEND_DIR = Path.cwd().parent / "frontend"
    if not FRONTEND_DIR.exists():
        FRONTEND_DIR = Path.cwd() / "frontend"

logger.info(f"Frontend directory: {FRONTEND_DIR}")


def seed_database_if_needed():
    """Seed the database with initial puzzles if empty."""
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.models.puzzle import Puzzle

    db = SessionLocal()
    try:
        # Check if puzzles exist
        puzzle_count = db.query(Puzzle).count()
        if puzzle_count == 0:
            logger.info("No puzzles found, seeding database...")
            # Import and run seed data
            import sys
            sys.path.insert(0, str(BACKEND_DIR))
            from seed_data import seed_puzzles
            seed_puzzles(db)
            logger.info("Database seeded successfully")
        else:
            logger.info(f"Database already has {puzzle_count} puzzles")
    except Exception as e:
        logger.error(f"Error checking/seeding database: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting application...")
    init_db()
    logger.info("Database initialized")

    # Seed database if needed (for fresh deployments)
    seed_database_if_needed()

    yield
    # Shutdown
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.app_name,
    description="A daily mini crossword puzzle game",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow all origins for simplicity
# In production, you might want to restrict this to your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.routers import auth_router, puzzles_router, friends_router, leaderboard_router

app.include_router(auth_router, prefix="/api")
app.include_router(puzzles_router, prefix="/api")
app.include_router(friends_router, prefix="/api")
app.include_router(leaderboard_router, prefix="/api")

# Mount static files for frontend
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    logger.info(f"Mounted static files from {FRONTEND_DIR}")
else:
    logger.warning(f"Frontend directory not found at {FRONTEND_DIR}")


@app.get("/")
async def root():
    """Serve the main frontend page."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Daily Mini Crossword API", "docs": "/docs"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.app_name}


if __name__ == "__main__":
    import uvicorn

    # Use PORT from environment (Render sets this)
    port = int(os.environ.get("PORT", settings.port))

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
    )
