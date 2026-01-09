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


# Large puzzle set - 21 puzzles (3 weeks worth) with unique words
# Each puzzle has distinct vocabulary to avoid repetition within a week
PUZZLES = [
    # Week 1 - Day 1: 5x5 Easy
    {
        "title": "Morning Start",
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
            ["C", "A", "F", "E", "S"],
            ["A", ".", "O", ".", "T"],
            ["B", "R", "E", "A", "E"],
            ["S", ".", "A", ".", "A"],
            ["T", "E", "M", "P", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Coffee shops", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Region or zone", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Temporary workers (abbr)", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Taxi vehicles", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Thick mist", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Meat cuts", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 1 - Day 2: 5x5 Easy
    {
        "title": "Farm Life",
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
            {"number": 1, "clue": "Riding animal", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Loop knot", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Wool animals", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Egg layers", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Sleeping space", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Female sheep", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 1 - Day 3: 5x5 Easy
    {
        "title": "Dinner Time",
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
            ["B", "R", "E", "A", "D"],
            ["E", ".", "A", ".", "I"],
            ["E", "A", "T", "E", "N"],
            ["F", ".", "S", ".", "E"],
            ["S", "T", "Y", "L", "E"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Toast base", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Consumed", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Fashion", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Cattle meat", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Compass direction", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Had supper", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 1 - Day 4: 5x5 Easy
    {
        "title": "City Walk",
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
            ["S", "T", "O", "R", "E"],
            ["H", ".", "P", ".", "A"],
            ["O", "P", "E", "R", "A"],
            ["P", ".", "N", ".", "S"],
            ["S", "P", "E", "N", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Shop", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Singing drama", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Used money", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Retail places", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Unlocked", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Delete", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 1 - Day 5: 6x6 Medium
    {
        "title": "School Days",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["P", "E", "N", "C", "I", "L"],
            ["A", ".", "O", "L", ".", "E"],
            ["P", "A", "P", "E", "R", "S"],
            ["E", "R", "E", "R", "A", "S"],
            ["R", ".", "R", "K", ".", "E"],
            ["S", "T", "S", "S", "E", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Writing tool", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Documents", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Ages or times", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Gatherings", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Documents", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Pepper partner", "length": 6, "row": 0, "col": 2},
            {"number": 5, "clue": "Rents out", "length": 6, "row": 0, "col": 5},
        ],
    },
    # Week 1 - Day 6: 6x6 Medium
    {
        "title": "Garden Fresh",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["F", "L", "O", "W", "E", "R"],
            ["I", ".", "R", "A", ".", "O"],
            ["E", "A", "A", "T", "C", "S"],
            ["L", "I", "N", "E", "H", "E"],
            ["D", ".", "G", "R", ".", "S"],
            ["S", "T", "E", "M", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Garden bloom", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Had food", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Row or queue", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Plant parts", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Open areas", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Citrus fruit", "length": 6, "row": 0, "col": 2},
            {"number": 5, "clue": "Pink flower", "length": 6, "row": 0, "col": 5},
        ],
    },
    # Week 1 - Day 7: 7x7 Hard
    {
        "title": "Word Power",
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
            ["T", "E", "A", "C", "H", "E", "R"],
            ["R", ".", "L", ".", "A", ".", "E"],
            ["A", "L", "E", "R", "T", "E", "D"],
            ["I", ".", "R", ".", "E", ".", "U"],
            ["N", "E", "T", "W", "R", "O", "C"],
            ["E", ".", "S", ".", "S", ".", "E"],
            ["D", "E", "S", "E", "R", "T", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Educator", "length": 7, "row": 0, "col": 0},
            {"number": 3, "clue": "Warned", "length": 7, "row": 2, "col": 0},
            {"number": 5, "clue": "Web + letters", "length": 7, "row": 4, "col": 0},
            {"number": 7, "clue": "Dry wastelands", "length": 7, "row": 6, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Skilled", "length": 7, "row": 0, "col": 0},
            {"number": 2, "clue": "Notifications", "length": 7, "row": 0, "col": 2},
            {"number": 4, "clue": "Despises", "length": 7, "row": 0, "col": 4},
            {"number": 6, "clue": "Diminished", "length": 7, "row": 0, "col": 6},
        ],
    },
    # Week 2 - Day 1: 5x5 Easy
    {
        "title": "Music Box",
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
            ["P", "I", "A", "N", "O"],
            ["L", ".", "L", ".", "P"],
            ["A", "L", "T", "O", "E"],
            ["N", ".", "O", ".", "R"],
            ["S", "O", "N", "G", "A"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Keyboard instrument", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Voice range", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Musical piece", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Schemes", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "In total", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Musical drama", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 2 - Day 2: 5x5 Easy
    {
        "title": "Beach Day",
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
            ["W", "A", "V", "E", "S"],
            ["A", ".", "I", ".", "A"],
            ["T", "I", "D", "E", "N"],
            ["E", ".", "E", ".", "D"],
            ["R", "E", "S", "T", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Ocean motions", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Ocean rise/fall", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Relaxes", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "H2O", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Motion picture", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Beach grains", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 2 - Day 3: 5x5 Easy
    {
        "title": "Pet Corner",
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
            ["D", "O", "G", "G", "Y"],
            ["U", ".", "O", ".", "A"],
            ["C", "A", "T", "T", "R"],
            ["K", ".", "S", ".", "N"],
            ["S", "E", "E", "D", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Puppy", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Feline + T", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Plant starters", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Baby birds", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Baby goats", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "String", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 2 - Day 4: 5x5 Easy
    {
        "title": "Game On",
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
            ["C", "H", "E", "S", "S"],
            ["A", ".", "N", ".", "C"],
            ["R", "U", "D", "E", "O"],
            ["D", ".", "S", ".", "R"],
            ["S", "K", "I", "P", "E"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Board game", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Impolite", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Jump over", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Playing cards", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Concludes", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Points", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 2 - Day 5: 6x6 Medium
    {
        "title": "Kitchen Fun",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "P", "O", "O", "N", "S"],
            ["A", ".", "V", "A", ".", "T"],
            ["L", "A", "E", "N", "I", "E"],
            ["T", "R", "N", "D", "C", "R"],
            ["S", ".", "S", "A", ".", "E"],
            ["B", "A", "K", "E", "R", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Utensils", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Venue + letters", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Pull", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Bread makers", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Sodium chloride", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Stove top", "length": 6, "row": 0, "col": 2},
            {"number": 5, "clue": "More forceful", "length": 6, "row": 0, "col": 5},
        ],
    },
    # Week 2 - Day 6: 6x6 Medium
    {
        "title": "Travel Log",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["F", "L", "I", "G", "H", "T"],
            ["A", ".", "N", "U", ".", "R"],
            ["R", "O", "A", "D", "I", "A"],
            ["E", "V", "N", "E", "D", "V"],
            ["S", ".", "A", "S", ".", "E"],
            ["T", "R", "I", "P", "S", "L"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Plane journey", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Street", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Smoothed out", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Journeys", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Costs", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Hostels", "length": 6, "row": 0, "col": 2},
            {"number": 5, "clue": "Goes by car", "length": 6, "row": 0, "col": 5},
        ],
    },
    # Week 2 - Day 7: 7x7 Hard
    {
        "title": "Big Words",
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
            ["A", "I", "R", "P", "O", "R", "T"],
            ["C", ".", "E", ".", "V", ".", "R"],
            ["T", "R", "A", "I", "E", "R", "A"],
            ["O", ".", "D", ".", "N", ".", "I"],
            ["R", "I", "E", "R", "S", "E", "N"],
            ["S", ".", "R", ".", "T", ".", "S"],
            ["S", "P", "S", "E", "S", "T", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Plane terminal", "length": 7, "row": 0, "col": 0},
            {"number": 3, "clue": "Feature", "length": 7, "row": 2, "col": 0},
            {"number": 5, "clue": "More parched", "length": 7, "row": 4, "col": 0},
            {"number": 7, "clue": "Initials + more", "length": 7, "row": 6, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Performers", "length": 7, "row": 0, "col": 0},
            {"number": 2, "clue": "Book lovers", "length": 7, "row": 0, "col": 2},
            {"number": 4, "clue": "Happenings", "length": 7, "row": 0, "col": 4},
            {"number": 6, "clue": "Locomotives", "length": 7, "row": 0, "col": 6},
        ],
    },
    # Week 3 - Day 1: 5x5 Easy
    {
        "title": "Book Worm",
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
            ["N", "O", "V", "E", "L"],
            ["O", ".", "E", ".", "I"],
            ["T", "A", "L", "E", "N"],
            ["E", ".", "V", ".", "E"],
            ["S", "T", "E", "M", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Long story", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Story", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Plant stalks", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Memos", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Stage", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Rows", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 3 - Day 2: 5x5 Easy
    {
        "title": "Sports Fan",
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
            ["T", "E", "A", "M", "S"],
            ["R", ".", "R", ".", "P"],
            ["A", "I", "E", "N", "O"],
            ["C", ".", "A", ".", "R"],
            ["K", "I", "C", "K", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Groups", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Zone", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Boot the ball", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Path", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Regions", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Athletics", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 3 - Day 3: 5x5 Easy
    {
        "title": "Home Base",
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
            ["R", "O", "O", "F", "S"],
            ["O", ".", "P", ".", "T"],
            ["O", "V", "E", "N", "A"],
            ["M", ".", "N", ".", "I"],
            ["S", "T", "E", "E", "R"],
        ],
        "clues_across": [
            {"number": 1, "clue": "House tops", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "Baking appliance", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Guide", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Chambers", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Unlocked", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Steps", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 3 - Day 4: 5x5 Easy
    {
        "title": "Work Day",
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
            ["D", "E", "S", "K", "S"],
            ["R", ".", "E", ".", "T"],
            ["A", "S", "N", "D", "A"],
            ["W", ".", "T", ".", "F"],
            ["S", "H", "E", "E", "F"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Work tables", "length": 5, "row": 0, "col": 0},
            {"number": 3, "clue": "As + letters", "length": 5, "row": 2, "col": 0},
            {"number": 5, "clue": "Paper bundle", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Sketches", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Transmitted", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Workers", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Week 3 - Day 5: 6x6 Medium
    {
        "title": "Nature Hike",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["F", "O", "R", "E", "S", "T"],
            ["E", ".", "I", "D", ".", "R"],
            ["R", "O", "V", "E", "R", "E"],
            ["N", "A", "E", "N", "A", "E"],
            ["S", ".", "R", "T", ".", "S"],
            ["T", "R", "S", "E", "R", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Woods", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Wanderer", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Name + letters", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Tr + letters", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Plants", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Streams", "length": 6, "row": 0, "col": 2},
            {"number": 5, "clue": "Trunks", "length": 6, "row": 0, "col": 5},
        ],
    },
    # Week 3 - Day 6: 6x6 Medium
    {
        "title": "Art Class",
        "size": 6,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", ".", " ", " ", ".", " "],
            [" ", " ", " ", " ", " ", " "],
        ],
        "solution": [
            ["P", "A", "I", "N", "T", "S"],
            ["A", ".", "M", "E", ".", "K"],
            ["S", "K", "A", "T", "E", "E"],
            ["T", "E", "G", "A", "R", "T"],
            ["E", ".", "E", "L", ".", "C"],
            ["S", "T", "S", "E", "T", "H"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Colors", "length": 6, "row": 0, "col": 0},
            {"number": 3, "clue": "Glide on ice", "length": 6, "row": 2, "col": 0},
            {"number": 4, "clue": "Sticky substance", "length": 6, "row": 3, "col": 0},
            {"number": 6, "clue": "Initials + letters", "length": 6, "row": 5, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Doughs", "length": 6, "row": 0, "col": 0},
            {"number": 2, "clue": "Pictures", "length": 6, "row": 0, "col": 2},
            {"number": 5, "clue": "Drawings", "length": 6, "row": 0, "col": 5},
        ],
    },
    # Week 3 - Day 7: 7x7 Hard
    {
        "title": "Grand Finale",
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
            ["S", "T", "A", "R", "T", "E", "D"],
            ["T", ".", "L", ".", "R", ".", "E"],
            ["O", "P", "E", "R", "A", "T", "E"],
            ["R", ".", "R", ".", "V", ".", "S"],
            ["I", "D", "T", "E", "E", "L", "I"],
            ["E", ".", "S", ".", "L", ".", "G"],
            ["S", "P", "S", "E", "S", "T", "N"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Began", "length": 7, "row": 0, "col": 0},
            {"number": 3, "clue": "Function", "length": 7, "row": 2, "col": 0},
            {"number": 5, "clue": "ID + letters", "length": 7, "row": 4, "col": 0},
            {"number": 7, "clue": "Initials + rest", "length": 7, "row": 6, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Narratives", "length": 7, "row": 0, "col": 0},
            {"number": 2, "clue": "Changes", "length": 7, "row": 0, "col": 2},
            {"number": 4, "clue": "Journeys", "length": 7, "row": 0, "col": 4},
            {"number": 6, "clue": "Plans", "length": 7, "row": 0, "col": 6},
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
        print(f"  Added puzzle: {puzzle_data['title']} ({puzzle_data['size']}x{puzzle_data['size']}, {puzzle_data['difficulty']})")

    db.commit()
    print(f"Seeded {len(PUZZLES)} puzzles (3 weeks worth).")


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
