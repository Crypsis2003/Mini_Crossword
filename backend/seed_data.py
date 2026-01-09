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


# Valid mini crossword puzzles - each cell is part of both across and down words
# Standard 5x5 grids with minimal black squares, all real English words
PUZZLES = [
    # Puzzle 1: 5x5 - Easy (No black squares - all cells connected)
    {
        "title": "Morning Start",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "T", "A", "R", "E"],
            ["C", "A", "B", "I", "N"],
            ["A", "R", "E", "N", "A"],
            ["L", "E", "N", "D", "S"],
            ["P", "S", "S", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Gaze intently", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Small house", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Sports stadium", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Loans out", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Hey! (quietly)", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Hair on head", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Begins", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Lacking", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Crazy", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Rent again", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 2: 5x5 - Easy
    {
        "title": "Beach Day",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "A", "N", "D", "S"],
            ["H", "U", "M", "A", "N"],
            ["O", "P", "E", "R", "A"],
            ["R", "E", "N", "T", "S"],
            ["E", "D", "D", "Y", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Beach grains", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Person", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Musical drama", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Leases", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Whirlpools", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Coastline", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Grown-up", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Label", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Draws near", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Catches", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 3: 5x5 - Easy
    {
        "title": "Word Play",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["C", "R", "A", "S", "H"],
            ["L", "I", "V", "E", "R"],
            ["A", "D", "O", "R", "E"],
            ["S", "E", "N", "S", "E"],
            ["P", "S", "S", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Collision", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Organ or resident", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Love deeply", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Judgment", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Quiet attention-getter", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Groups or categories", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Horse riders", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Evade", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Not loose", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Listens to", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 4: 5x5 - Easy
    {
        "title": "City Life",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["T", "R", "A", "I", "N"],
            ["R", "I", "D", "E", "S"],
            ["A", "D", "D", "E", "D"],
            ["S", "E", "E", "R", "S"],
            ["H", "S", "S", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Subway vehicle", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Travels in a car", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Put in more", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Prophets", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Sound for quiet", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Garbage", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Motorcyclists", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Speech", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Odd", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Resting spots", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 5: 5x5 - Medium
    {
        "title": "Food Fun",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "P", "I", "C", "E"],
            ["T", "O", "N", "E", "R"],
            ["E", "P", "I", "C", "S"],
            ["A", "E", "N", "A", "L"],
            ["K", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Seasoning", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Printer supply", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Grand tales", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Kidney-related", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Hissing sounds", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Meat cuts", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Begins (a door)", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Lodging places", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Film locations", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Cuts in two", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 6: 5x5 - Medium
    {
        "title": "Pet Shop",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["C", "A", "G", "E", "S"],
            ["A", "L", "O", "N", "E"],
            ["T", "O", "N", "I", "C"],
            ["S", "N", "A", "C", "K"],
            ["H", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Bird enclosures", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Solitary", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Gin mixer", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Light bite", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Snake sounds", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Felines", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "On the way", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Previously", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Penny", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Bags (paper)", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 7: 5x5 - Medium
    {
        "title": "Game Night",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["P", "L", "A", "Y", "S"],
            ["R", "I", "V", "E", "R"],
            ["I", "N", "E", "R", "T"],
            ["C", "E", "N", "T", "S"],
            ["E", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Theater shows", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Flowing water", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Not reactive", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Pennies", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Plural of S", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Cost", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Queue", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Streets", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Yearly books", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Begins", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 8: 5x5 - Medium
    {
        "title": "Nature Walk",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["T", "R", "E", "E", "S"],
            ["H", "O", "N", "E", "Y"],
            ["A", "N", "G", "E", "R"],
            ["W", "E", "S", "T", "S"],
            ["S", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Forest plants", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Sweet syrup", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Fury", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Compass directions", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Plural suffix sound", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Melts", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "One person", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Motor parts", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Consume", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Yell", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 9: 5x5 - Hard
    {
        "title": "Brain Teaser",
        "size": 5,
        "difficulty": "hard",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["G", "R", "A", "S", "P"],
            ["R", "O", "U", "T", "E"],
            ["A", "U", "D", "I", "O"],
            ["S", "T", "I", "L", "T"],
            ["P", "E", "O", "N", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Understand or grip", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Road or path", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Sound system", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Walking pole", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Low workers", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Green plants", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Fight results", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Sound systems", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "However", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Writing tools", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 10: 5x5 - Hard
    {
        "title": "Word Master",
        "size": 5,
        "difficulty": "hard",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "P", "A", "R", "E"],
            ["T", "O", "N", "I", "C"],
            ["A", "R", "E", "N", "A"],
            ["R", "E", "W", "E", "D"],
            ["E", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Extra or lean", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Fizzy water", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Sports venue", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Sewed again", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Letter sounds", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Heavenly bodies", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Harbors", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Reply", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Matured", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Skilled", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 11: 5x5 - Hard
    {
        "title": "Challenge",
        "size": 5,
        "difficulty": "hard",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "T", "O", "R", "E"],
            ["T", "I", "D", "E", "S"],
            ["A", "G", "E", "N", "T"],
            ["G", "E", "A", "R", "S"],
            ["E", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Shop", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Ocean flows", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Spy or rep", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Equipment", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Hissing", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Theater phases", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Felines", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Notions", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Makes money", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Checks", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 12: 5x5 - Hard
    {
        "title": "Grand Finale",
        "size": 5,
        "difficulty": "hard",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["B", "L", "A", "S", "T"],
            ["R", "I", "V", "E", "R"],
            ["A", "V", "E", "R", "S"],
            ["I", "N", "E", "T", "S"],
            ["N", "E", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Explosion", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Stream", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "States firmly", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Fish traps", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "State suffix", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Mind", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Surviving", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Typical", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Makes steady", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Experiments", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Additional puzzles for practice mode - varied difficulties
    # Puzzle 13: Practice - Easy
    {
        "title": "Quick Quiz",
        "size": 5,
        "difficulty": "easy",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["B", "R", "E", "A", "D"],
            ["L", "O", "V", "E", "R"],
            ["A", "V", "E", "N", "T"],
            ["R", "E", "N", "D", "S"],
            ["E", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Sliced loaf", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Romantic partner", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Happening", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Stylish", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Letter sound", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Glare", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Stoves", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Forever", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Finishes", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Tears", "length": 5, "row": 0, "col": 4},
        ],
    },
    # Puzzle 14: Practice - Medium
    {
        "title": "Think Fast",
        "size": 5,
        "difficulty": "medium",
        "grid": [
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
        ],
        "solution": [
            ["S", "L", "A", "T", "E"],
            ["C", "O", "V", "E", "R"],
            ["A", "R", "E", "N", "A"],
            ["R", "E", "N", "D", "S"],
            ["S", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Chalkboard", "length": 5, "row": 0, "col": 0},
            {"number": 6, "clue": "Hide or lid", "length": 5, "row": 1, "col": 0},
            {"number": 7, "clue": "Stadium", "length": 5, "row": 2, "col": 0},
            {"number": 8, "clue": "Gives", "length": 5, "row": 3, "col": 0},
            {"number": 9, "clue": "Sibilants", "length": 5, "row": 4, "col": 0},
        ],
        "clues_down": [
            {"number": 1, "clue": "Frightens", "length": 5, "row": 0, "col": 0},
            {"number": 2, "clue": "Lords", "length": 5, "row": 0, "col": 1},
            {"number": 3, "clue": "Paths", "length": 5, "row": 0, "col": 2},
            {"number": 4, "clue": "Renters", "length": 5, "row": 0, "col": 3},
            {"number": 5, "clue": "Listens", "length": 5, "row": 0, "col": 4},
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
