# Daily Mini Crossword

A full-stack web application for playing daily crossword puzzles, built with FastAPI and vanilla JavaScript.

## Features

- **Daily Puzzles**: Each day features a new crossword puzzle (5x5 to 7x7 grid)
- **Interactive Gameplay**:
  - Click cells or clues to navigate
  - Arrow keys for movement
  - Tab to jump between words
  - Space bar to toggle direction (across/down)
- **Timer**: Tracks solve time, starts on first input
- **User Accounts**: Register, login, and track your progress
- **Friends System**: Add friends and compare scores
- **Leaderboards**: See how you rank globally and among friends
- **Share Results**: Wordle-style share text for completed puzzles

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM with SQLite (PostgreSQL-ready)
- **Alembic** - Database migrations
- **JWT** - Token-based authentication
- **Pydantic** - Data validation
- **Bcrypt** - Password hashing

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **CSS3** - Custom styling with CSS variables
- **Responsive Design** - Works on desktop and mobile

## Project Structure

```
Mini_Crossword/
├── backend/
│   ├── app/
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── utils/        # Helpers (auth, security)
│   │   ├── config.py     # Settings management
│   │   ├── database.py   # Database setup
│   │   └── main.py       # FastAPI application
│   ├── alembic/          # Database migrations
│   ├── tests/            # Test suite
│   ├── seed_data.py      # Sample data loader
│   └── requirements.txt
├── frontend/
│   ├── css/style.css     # Styles
│   ├── js/
│   │   ├── api.js        # API client
│   │   ├── auth.js       # Authentication
│   │   ├── crossword.js  # Game logic
│   │   └── app.js        # Main application
│   └── index.html        # Main page
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── README.md
```

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Start the application
docker compose up --build

# Access at http://localhost:8000
```

### Option 2: Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
make install
# or: cd backend && pip install -r requirements.txt

# 3. Run the application
make run
# or: cd backend && python seed_data.py && uvicorn app.main:app --port 8000

# Access at http://localhost:8000
```

### Option 3: Development Mode (with auto-reload)

```bash
make dev
```

### Option 4: Deploy to Render (Production)

Deploy to [Render](https://render.com) with a free PostgreSQL database:

```bash
# Push to GitHub, then on Render:
# 1. New → Blueprint
# 2. Connect your repo
# 3. Render detects render.yaml and deploys automatically
```

See **[README_DEPLOY.md](README_DEPLOY.md)** for detailed deployment instructions.

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get tokens |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Get current user |
| GET | `/api/auth/profile` | Get user profile with stats |
| POST | `/api/auth/logout` | Logout |

### Puzzles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/puzzles/today` | Get today's puzzle |
| GET | `/api/puzzles/{id}` | Get puzzle by ID |
| GET | `/api/puzzles/date/{date}` | Get puzzle by date |
| POST | `/api/puzzles/{id}/check` | Check solution |
| POST | `/api/puzzles/{id}/solve` | Submit solve |
| GET | `/api/puzzles/{id}/my-solve` | Get user's solve |

### Friends
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/friends` | Get friends list |
| POST | `/api/friends/request` | Send friend request |
| POST | `/api/friends/request/{id}/accept` | Accept request |
| POST | `/api/friends/request/{id}/reject` | Reject request |
| DELETE | `/api/friends/{id}` | Remove friend |
| GET | `/api/friends/search?q=` | Search users |

### Leaderboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leaderboard/today` | Today's leaderboard |
| GET | `/api/leaderboard/puzzle/{id}` | Puzzle leaderboard |
| GET | `/api/leaderboard/friends/today` | Friends leaderboard |

## Running Tests

```bash
make test
# or: cd backend && pytest tests/ -v
```

## Database

### SQLite (Default)
The application uses SQLite by default, storing data in `backend/crossword.db`.

### PostgreSQL (Production)

1. Update `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/crossword
```

2. Uncomment PostgreSQL service in `docker-compose.yml`

3. Add PostgreSQL driver:
```bash
pip install psycopg2-binary
```

### Migrations

```bash
# Apply migrations
make migrate

# Create new migration
make migration msg="Add new field"
```

## Sample Users

After running `seed_data.py`, these test accounts are available:

| Username | Password |
|----------|----------|
| alice | password123 |
| bob | password123 |
| charlie | password123 |

## Configuration

Create a `.env` file (copy from `.env.example`):

```env
# Application
APP_NAME=Daily Mini Crossword
DEBUG=true
SECRET_KEY=your-secret-key-min-32-characters

# Database
DATABASE_URL=sqlite:///./crossword.db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Server
HOST=0.0.0.0
PORT=8000
```

## Design Decisions

### Authentication
- **JWT tokens** stored in localStorage
- Access tokens expire in 30 minutes
- Refresh tokens for seamless re-authentication
- Passwords hashed with bcrypt

### Puzzle Selection
- Puzzles can be scheduled for specific dates
- Unscheduled puzzles are selected deterministically by date hash
- This ensures the same puzzle appears for all users on a given day

### Friend System
- Request/accept model (not instant add)
- Bidirectional friendships stored for query efficiency
- Users can see friends' solve times on leaderboards

### Anonymous vs Authenticated Play
- Anyone can view and play puzzles
- Only authenticated users can save solve times
- Leaderboard participation requires login

## Keyboard Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Navigate between cells |
| Tab | Jump to next word |
| Shift+Tab | Jump to previous word |
| Space | Toggle direction (across/down) |
| Backspace | Clear cell and move back |
| Letters | Enter letter and advance |

## Future Enhancements

- [ ] Puzzle generator (currently uses templates)
- [ ] Dark mode
- [ ] Streak tracking
- [ ] Achievement badges
- [ ] Daily email notifications
- [ ] Mobile app (React Native)

## License

MIT License - feel free to use and modify.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request
