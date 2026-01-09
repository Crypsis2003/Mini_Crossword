"""Seed data script to populate the database with sample puzzles."""

import json
import sys
from datetime import date, timedelta

# Add the app directory to the path
sys.path.insert(0, ".")

from app.database import SessionLocal, init_db
from app.models.puzzle import Puzzle
from app.models.user import User
from app.utils.security import hash_password


# Sample puzzles - 12 puzzles of varying sizes (5x5, 6x6, 7x7)
PUZZLES = [
    # Puzzle 1: 5x5
    {
        "title": "Morning Brew",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["C", "O", "F", "F", "E"],
            ["A", ".", "O", ".", "A"],
            ["B", "R", "E", "A", "D"],
            ["S", ".", "G", ".", "R"],
            ["T", "E", "A", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Morning beverage with caffeine", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Sliced for toast", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Breakfast beverage (or crispy bread)", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Taxi transport", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Thick mist", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Start the day ___", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 2: 5x5
    {
        "title": "Pet Parade",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", ".", ".", ".", " "],
            [" ", " ", " ", " ", " "],
            [" ", ".", ".", ".", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["C", "A", "T", "S", "O"],
            ["A", ".", ".", ".", "W"],
            ["P", "A", "W", "E", "L"],
            ["E", ".", ".", ".", "S"],
            ["D", "O", "G", "S", "Y"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Feline pets, plus a direction", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Animal foot + proper name", "length": 5, "row": 2, "col": 0},
            {"number": 4, "clue": "Canine pets + affirmative", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Superhero outfit accessory", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Night birds", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 3: 5x5
    {
        "title": "Color Mix",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["B", "L", "U", "E", "S"],
            ["E", ".", "N", ".", "H"],
            ["G", "R", "E", "E", "N"],
            ["A", ".", "A", ".", "Y"],
            ["N", "O", "R", "T", "H"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Sad music genre", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Grass color", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Cardinal direction", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Start (a journey)", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Without clothes", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Bright and sunny", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 4: 6x6
    {
        "title": "Kitchen Tools",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "P", "O", "O", "N", "S"],
            ["P", ".", "V", ".", "I", "T"],
            ["A", "R", "E", "N", "A", "E"],
            ["T", "E", "N", "D", "E", "R"],
            ["U", "D", ".", "S", ".", "E"],
            ["L", "A", "I", "T", "Y", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Soup utensils", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Sports stadium", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Soft and gentle", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Non-clergy members", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Kitchen tool that flips", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Cooked in the oven", "length": 6, "row": 0, "col": 2},
            {"number": 5, "clue": "Trees or forests", "length": 6, "row": 0, "col": 5},
        ],
    },
    # Puzzle 5: 6x6
    {
        "title": "Music Time",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["P", "I", "A", "N", "O", "S"],
            ["L", ".", ".", "O", ".", "O"],
            ["A", "L", "B", "U", "M", "S"],
            ["Y", "U", "N", "D", "E", "R"],
            ["S", ".", "O", ".", ".", "K"],
            ["G", "U", "I", "T", "A", "R"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Keyboard instruments", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Music collections", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Beneath", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Six-stringed instrument", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Drama performances", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Loud + rhythm = ?", "length": 6, "row": 0, "col": 3},
            {"number": 5, "clue": "Drenched", "length": 6, "row": 0, "col": 5},
        ],
    },
    # Puzzle 6: 6x6
    {
        "title": "Weather Watch",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", ".", " ", " ", "." ],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [".", " ", " ", ".", " ", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "T", "O", "R", "M", "Y"],
            ["U", "A", ".", "A", "O", "."],
            ["N", "L", "I", "N", "K", "S"],
            ["N", "E", "W", "E", "Y", "O"],
            [".", "N", "I", ".", "S", "A"],
            ["C", "T", "N", "D", "E", "K"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Turbulent weather", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Golf course connections", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Fresh + positive", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Clink + D sounds like?", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Bright and happy", "length": 4, "row": 0, "col": 0},
            {"number": 2, "clue": "Gift, ability", "length": 6, "row": 0, "col": 1},
            {"number": 5, "clue": "Primate + letters", "length": 6, "row": 0, "col": 4},
        ],
    },
    # Puzzle 7: 7x7
    {
        "title": "World Travel",
        "size": 7,
        "difficulty": "hard",
        "grid": [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["F", "R", "A", "N", "C", "E", "S"],
            ["L", ".", "R", ".", "H", ".", "P"],
            ["I", "T", "A", "L", "I", "N", "A"],
            ["G", ".", "B", ".", "N", ".", "I"],
            ["H", "E", "I", "R", "E", "D", "N"],
            ["T", ".", "A", ".", "S", ".", "S"],
            ["S", "W", "N", "A", "E", "R", "O"],
        ],
        "clues_across": [
            {"number": 1, "clue": "European country + name", "length": 7, "row": 0, "col": 0},
            {"number": 3, "clue": "Mediterranean country + word", "length": 7, "row": 2, "col": 0},
            {"number": 5, "clue": "Received inheritance", "length": 7, "row": 4, "col": 0},
            {"number": 7, "clue": "Swan + cookie brand", "length": 7, "row": 6, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Airplane journeys", "length": 7, "row": 0, "col": 0},
            {"number": 2, "clue": "Middle Eastern + countries", "length": 7, "row": 0, "col": 2},
            {"number": 4, "clue": "Asia country + letters", "length": 7, "row": 0, "col": 4},
            {"number": 6, "clue": "European country", "length": 7, "row": 0, "col": 6},
        ],
    },
    # Puzzle 8: 7x7
    {
        "title": "Food Fest",
        "size": 7,
        "difficulty": "hard",
        "grid": [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", ".", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["P", "A", "S", "T", "A", "S", "Y"],
            ["I", ".", "A", "O", "P", ".", "O"],
            ["Z", "E", "L", "M", "P", "R", "G"],
            ["Z", "A", "A", ".", "L", "I", "U"],
            ["A", "T", "M", "E", "E", "C", "R"],
            ["S", ".", "O", "A", "S", ".", "T"],
            ["B", "R", "N", "T", "Y", "E", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Italian noodle dishes + letter", "length": 7, "row": 0, "col": 0},
            {"number": 3, "clue": "Name + cooking style", "length": 7, "row": 2, "col": 0},
            {"number": 5, "clue": "Person who eats + letters", "length": 7, "row": 4, "col": 0},
            {"number": 7, "clue": "Bread + extra letters", "length": 7, "row": 6, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Flat Italian pies", "length": 7, "row": 0, "col": 0},
            {"number": 2, "clue": "Spice + seasoning", "length": 7, "row": 0, "col": 2},
            {"number": 4, "clue": "Fruit + extras", "length": 7, "row": 0, "col": 4},
            {"number": 6, "clue": "Dairy product", "length": 7, "row": 0, "col": 6},
        ],
    },
    # Puzzle 9: 5x5
    {
        "title": "Animal Farm",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["H", "O", "R", "S", "E"],
            ["E", ".", "O", ".", "W"],
            ["N", "O", "O", "S", "E"],
            ["S", ".", "M", ".", "S"],
            ["S", "H", "E", "E", "P"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Farm animal for riding", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "A loop knot", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Wool-producing animals", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Female chickens", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Bedroom space", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Female sheep (plural)", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 10: 5x5
    {
        "title": "Sports Day",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["T", "E", "N", "I", "S"],
            ["E", ".", "I", ".", "W"],
            ["A", "R", "G", "U", "E"],
            ["M", ".", "H", ".", "E"],
            ["S", "O", "T", "T", "O"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Racket sport (variant spelling)", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Dispute verbally", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Under (Italian)", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Sports group", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Evening hours", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Perspiration + letters", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 11: 6x6
    {
        "title": "Garden Party",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["F", "L", "O", "W", "E", "R"],
            ["L", ".", "N", ".", "A", "O"],
            ["O", "W", "E", "D", "R", "S"],
            ["W", "A", "V", "E", "S", "E"],
            ["E", "R", ".", "D", ".", "S"],
            ["R", "E", "E", "D", "S", "Y"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Garden bloom", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Had a debt", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Ocean motions", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Tall water plants + letter", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Garden blooms (another word)", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Single + word", "length": 6, "row": 0, "col": 2},
            {"number": 5, "clue": "Pink flower + letters", "length": 6, "row": 0, "col": 4},
        ],
    },
    # Puzzle 12: 7x7
    {
        "title": "City Life",
        "size": 7,
        "difficulty": "hard",
        "grid": [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", ".", " ", ".", " ", ".", " "],
            [" ", " ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["T", "R", "A", "F", "F", "I", "C"],
            ["A", ".", "S", ".", "L", ".", "O"],
            ["X", "E", "P", "H", "A", "L", "T"],
            ["I", ".", "H", ".", "T", ".", "E"],
            ["S", "T", "A", "T", "E", "L", "Y"],
            ["T", ".", "L", ".", "N", ".", "O"],
            ["O", "U", "T", "L", "E", "T", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Cars on the road", "length": 7, "row": 0, "col": 0},
            {"number": 3, "clue": "Road surface (misspelled)", "length": 7, "row": 2, "col": 0},
            {"number": 5, "clue": "Grand and dignified", "length": 7, "row": 4, "col": 0},
            {"number": 7, "clue": "Shopping stores", "length": 7, "row": 6, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Cab drivers", "length": 7, "row": 0, "col": 0},
            {"number": 2, "clue": "Road surface material", "length": 7, "row": 0, "col": 2},
            {"number": 4, "clue": "Smooth out", "length": 7, "row": 0, "col": 4},
            {"number": 6, "clue": "Baby beds", "length": 7, "row": 0, "col": 6},
        ],
    },
]


def seed_puzzles(db):
    """Seed the database with sample puzzles."""
    print("Seeding puzzles...")

    for i, puzzle_data in enumerate(PUZZLES):
        # Check if puzzle already exists
        existing = db.query(Puzzle).filter(Puzzle.title == puzzle_data["title"]).first()
        if existing:
            print(f"  Puzzle '{puzzle_data['title']}' already exists, skipping...")
            continue

        puzzle = Puzzle(
            title=puzzle_data["title"],
            size=puzzle_data["size"],
            difficulty=puzzle_data["difficulty"],
            grid=json.dumps(puzzle_data["grid"]),
            solution=json.dumps(puzzle_data["solution"]),
            clues_across=json.dumps(puzzle_data["clues_across"]),
            clues_down=json.dumps(puzzle_data["clues_down"]),
            scheduled_date=None,  # Unscheduled - will be selected by date hash
        )

        db.add(puzzle)
        print(f"  Added puzzle: {puzzle_data['title']} ({puzzle_data['size']}x{puzzle_data['size']})")

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
        print("\nSample login credentials:")
        print("  Username: alice, Password: password123")
        print("  Username: bob, Password: password123")
        print("  Username: charlie, Password: password123")
    finally:
        db.close()


if __name__ == "__main__":
    main()
