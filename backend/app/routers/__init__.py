"""API routers."""

from app.routers.auth import router as auth_router
from app.routers.puzzles import router as puzzles_router
from app.routers.friends import router as friends_router
from app.routers.leaderboard import router as leaderboard_router

__all__ = ["auth_router", "puzzles_router", "friends_router", "leaderboard_router"]
