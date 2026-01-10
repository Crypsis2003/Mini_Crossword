# Mini Crossword Backend

FastAPI backend for the Daily Mini Crossword game.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file or set these variables:
```bash
DATABASE_URL=sqlite:///./crossword.db  # or PostgreSQL URL
SECRET_KEY=your-secret-key-here
DEBUG=false
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Generate Puzzles
```bash
python manage.py generate
```

### 5. Start the Server
```bash
uvicorn app.main:app --reload
```

## Management Commands

All management is done through `manage.py`:

```bash
# Generate puzzles for the current week
python manage.py generate

# Force refresh puzzles (delete and regenerate)
python manage.py refresh

# Refresh a specific week
python manage.py refresh --week 2026-W03

# List all puzzles in database
python manage.py list

# Run database migrations
python manage.py migrate

# Test puzzle generation (doesn't save)
python manage.py test
```

## After Deployment

Run this command after each deployment to ensure puzzles are generated:
```bash
python manage.py generate
```

Or to force refresh:
```bash
python manage.py refresh
```

## API Endpoints

### Puzzles
- `GET /api/puzzles/today` - Get today's puzzle
- `GET /api/puzzles/{id}` - Get puzzle by ID
- `GET /api/puzzles/date/{date}` - Get puzzle for specific date
- `POST /api/puzzles/{id}/check` - Check solution
- `POST /api/puzzles/{id}/solve` - Submit solve (requires auth)
- `POST /api/puzzles/refresh` - Force refresh puzzles (admin)

### Auth
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Leaderboard
- `GET /api/leaderboard/{puzzle_id}` - Get leaderboard for puzzle
- `GET /api/leaderboard/{puzzle_id}/friends` - Get friends leaderboard

### Friends
- `POST /api/friends/request` - Send friend request
- `POST /api/friends/accept/{id}` - Accept friend request
- `GET /api/friends` - List friends

## Puzzle Generation

Puzzles are generated with:
- 5x5 grid with 1-5 black squares
- All words validated against English dictionary
- Different pattern each day
- Automatic clue generation for common words

The dictionary is automatically downloaded on first run from a public word list.

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── database.py          # DB setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API routes
│   ├── services/            # Business logic
│   │   ├── puzzle_cache.py      # Weekly puzzle generation
│   │   ├── puzzle_templates.py  # Validated puzzle generator
│   │   └── ...
│   └── utils/               # Utilities
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── manage.py               # Management script
└── requirements.txt        # Dependencies
```
