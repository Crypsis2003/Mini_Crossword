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


def seed_database_if_needed():
    """Seed the database with initial puzzles if empty."""
    from app.database import SessionLocal
    from app.models.puzzle import Puzzle

    db = SessionLocal()
    try:
        puzzle_count = db.query(Puzzle).count()
        if puzzle_count == 0:
            logger.info("No puzzles found, seeding database...")
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
    logger.info("Starting application...")
    init_db()
    logger.info("Database initialized")
    seed_database_if_needed()
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
