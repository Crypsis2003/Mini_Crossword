"""Test configuration and fixtures."""

import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User, Puzzle
from app.utils.security import hash_password

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_user(db):
    """Create a sample user."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_user2(db):
    """Create a second sample user."""
    user = User(
        username="testuser2",
        email="test2@example.com",
        hashed_password=hash_password("password123"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_puzzle(db):
    """Create a sample puzzle."""
    puzzle = Puzzle(
        title="Test Puzzle",
        size=5,
        difficulty="easy",
        grid=json.dumps([
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
        ]),
        solution=json.dumps([
            ["H", "E", "L", "L", "O"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]),
        clues_across=json.dumps([
            {"number": 1, "clue": "Greeting", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Tranquility", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Affirmatives", "length": 5, "row": 4, "col": 0},
        ]),
        clues_down=json.dumps([
            {"number": 1, "clue": "Joyful", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Deceiver", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Single items", "length": 5, "row": 0, "col": 4},
        ]),
    )
    db.add(puzzle)
    db.commit()
    db.refresh(puzzle)
    return puzzle


@pytest.fixture
def auth_headers(client, sample_user):
    """Get auth headers for the sample user."""
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers2(client, sample_user2):
    """Get auth headers for the second sample user."""
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser2", "password": "password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
