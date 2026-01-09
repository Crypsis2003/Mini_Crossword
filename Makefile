# Makefile for Daily Mini Crossword

.PHONY: help install run dev test seed migrate docker-up docker-down clean

# Default target
help:
	@echo "Daily Mini Crossword - Available Commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the application"
	@echo "  make dev        - Run in development mode with auto-reload"
	@echo "  make test       - Run tests"
	@echo "  make seed       - Seed the database with sample data"
	@echo "  make migrate    - Run database migrations"
	@echo "  make docker-up  - Start with Docker Compose"
	@echo "  make docker-down- Stop Docker containers"
	@echo "  make clean      - Remove generated files"
	@echo ""

# Install dependencies
install:
	cd backend && pip install -r requirements.txt

# Run the application
run:
	cd backend && python seed_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run in development mode
dev:
	cd backend && python seed_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
test:
	cd backend && pytest tests/ -v

# Seed the database
seed:
	cd backend && python seed_data.py

# Run database migrations
migrate:
	cd backend && alembic upgrade head

# Create a new migration
migration:
	cd backend && alembic revision --autogenerate -m "$(msg)"

# Start with Docker
docker-up:
	docker compose up --build

# Stop Docker containers
docker-down:
	docker compose down

# Clean generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -f backend/crossword.db 2>/dev/null || true
	rm -rf backend/.pytest_cache 2>/dev/null || true
