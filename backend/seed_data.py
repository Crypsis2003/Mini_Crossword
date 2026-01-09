"""Seed data script to populate the database with sample puzzles."""

import json
import sys
from datetime import date, timedelta

sys.path.insert(0, ".")

from app.database import SessionLocal, init_db
from app.models.puzzle import Puzzle
from app.models.user import User
from app.utils.security import hash_password


# Valid mini crossword puzzles - every row AND column is a real word
# Black square at [0][0] creates symmetric grids
PUZZLES = [
    # Puzzle 1: STEW grid
    {
        "title": "Kitchen Classics",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "S", "T", "E", "W"],
            ["S", "T", "O", "R", "E"],
            ["T", "O", "R", "E", "S"],
            ["E", "R", "E", "C", "T"],
            ["W", "E", "S", "T", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Hearty soup dish", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "Shop or keep", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "Rips apart", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Build or upright", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Western directions", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Hearty soup dish", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "Shop or keep", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Rips apart", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Build or upright", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Western directions", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 2: SCAR grid
    {
        "title": "Battle Marks",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "S", "C", "A", "R"],
            ["S", "C", "A", "R", "E"],
            ["C", "A", "R", "E", "R"],
            ["A", "R", "E", "N", "A"],
            ["R", "E", "R", "A", "N"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Wound mark", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "Frighten", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "One who provides care", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Sports stadium", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Ran again", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Wound mark", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "Frighten", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "One who provides care", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Sports stadium", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Ran again", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 3: RACE grid (includes Max Ernst)
    {
        "title": "Art & Speed",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "R", "A", "C", "E"],
            ["R", "A", "C", "E", "R"],
            ["A", "C", "O", "R", "N"],
            ["C", "E", "R", "E", "S"],
            ["E", "R", "N", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Competition of speed", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "One who competes for speed", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "Oak tree seed", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Roman goddess of harvest", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Surrealist painter Max ___", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Competition of speed", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "One who competes for speed", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Oak tree seed", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Roman goddess of harvest", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Surrealist painter Max ___", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 4: PAST grid
    {
        "title": "Time Gone By",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "P", "A", "S", "T"],
            ["P", "A", "S", "T", "E"],
            ["A", "S", "T", "E", "R"],
            ["S", "T", "E", "R", "N"],
            ["T", "E", "R", "N", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Gone by in time", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "Glue or spread", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "Star-shaped flower", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Rear of a ship", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Arctic birds", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Gone by in time", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "Glue or spread", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Star-shaped flower", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Rear of a ship", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Arctic birds", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 5: FARE grid
    {
        "title": "Travel Costs",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "F", "A", "R", "E"],
            ["F", "A", "R", "E", "R"],
            ["A", "R", "E", "N", "A"],
            ["R", "E", "N", "D", "S"],
            ["E", "R", "A", "S", "E"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Bus or taxi price", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "One who pays to travel", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "Concert venue", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Tears apart", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Delete completely", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Bus or taxi price", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "One who pays to travel", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Concert venue", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Tears apart", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Delete completely", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 6: CAST grid
    {
        "title": "Theater Night",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "C", "A", "S", "T"],
            ["C", "A", "S", "T", "E"],
            ["A", "S", "T", "E", "R"],
            ["S", "T", "E", "R", "N"],
            ["T", "E", "R", "N", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Actors in a play", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "Social class system", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "Daisy-like flower", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Serious or strict", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Seabirds", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Actors in a play", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "Social class system", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Daisy-like flower", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Serious or strict", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Seabirds", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 7: SPAR grid
    {
        "title": "Boxing Ring",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "S", "P", "A", "R"],
            ["S", "P", "A", "R", "E"],
            ["P", "A", "R", "E", "R"],
            ["A", "R", "E", "N", "A"],
            ["R", "E", "R", "A", "N"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Practice boxing", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "Extra or leftover", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "Fruit peeling tool", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Gladiator's battleground", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Competed again in a race", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Practice boxing", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "Extra or leftover", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Fruit peeling tool", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Gladiator's battleground", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Competed again in a race", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 8: RARE grid
    {
        "title": "Uncommon Finds",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "R", "A", "R", "E"],
            ["R", "A", "R", "E", "R"],
            ["A", "R", "E", "N", "A"],
            ["R", "E", "N", "D", "S"],
            ["E", "R", "A", "S", "E"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Not common", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "More uncommon", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "Sports complex", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Splits or tears", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Wipe out", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Not common", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "More uncommon", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Sports complex", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Splits or tears", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Wipe out", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 9: BAST grid
    {
        "title": "Natural Fibers",
        "size": 5,
        "difficulty": "hard",
        "grid": [
            [".", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            [".", "B", "A", "S", "T"],
            ["B", "A", "S", "T", "E"],
            ["A", "S", "T", "E", "R"],
            ["S", "T", "E", "R", "N"],
            ["T", "E", "R", "N", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Plant fiber for rope", "length": 4, "row": 0, "col": 1},
            {"number": 5, "clue": "Moisten while roasting", "length": 5, "row": 1, "col": 0},
            {"number": 6, "clue": "Fall blooming flower", "length": 5, "row": 2, "col": 0},
            {"number": 7, "clue": "Back of a boat", "length": 5, "row": 3, "col": 0},
            {"number": 8, "clue": "Arctic seabirds", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Plant fiber for rope", "length": 4, "row": 1, "col": 0},
            {"number": 2, "clue": "Moisten while roasting", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Fall blooming flower", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Back of a boat", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Arctic seabirds", "length": 5, "row": 0, "col": 4},
        ],
    },
]


def seed_puzzles(db):
    """Seed the database with sample puzzles."""
    print("Clearing existing puzzles...")
    db.query(Puzzle).delete()
    db.commit()

    print("Seeding puzzles...")
    for i, puzzle_data in enumerate(PUZZLES):
        puzzle = Puzzle(
            title=puzzle_data["title"],
            size=puzzle_data["size"],
            difficulty=puzzle_data["difficulty"],
            grid=json.dumps(puzzle_data["grid"]),
            solution=json.dumps(puzzle_data["solution"]),
            clues_across=json.dumps(puzzle_data["clues_across"]),
            clues_down=json.dumps(puzzle_data["clues_down"]),
            scheduled_date=None,
        )
        db.add(puzzle)
        print(f"  Added: {puzzle_data['title']} ({puzzle_data['difficulty']})")

    db.commit()
    print(f"Seeded {len(PUZZLES)} puzzles.")


def seed_sample_users(db):
    """Seed some sample users for testing."""
    print("Seeding sample users...")
    sample_users = [
        {"username": "alice", "email": "alice@example.com", "password": "password123"},
        {"username": "bob", "email": "bob@example.com", "password": "password123"},
        {"username": "charlie", "email": "charlie@example.com", "password": "password123"},
    ]

    for user_data in sample_users:
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if existing:
            print(f"  User '{user_data['username']}' already exists, skipping...")
            continue

        user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"]),
        )
        db.add(user)
        print(f"  Added user: {user_data['username']}")

    db.commit()
    print("Seeded sample users.")


def main():
    """Main seeding function."""
    print("Initializing database...")
    init_db()

    db = SessionLocal()
    try:
        seed_puzzles(db)
        seed_sample_users(db)
        print("\nSeeding complete!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
