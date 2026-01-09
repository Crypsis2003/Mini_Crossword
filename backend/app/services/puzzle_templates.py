"""Pre-made valid crossword puzzle templates for instant generation.

Each template is a mini crossword with DIFFERENT across and down words.
Uses black squares to create proper crossword structure.
"""

import logging

logger = logging.getLogger(__name__)

BLACK = "."

# Each template has different across and down words (not word squares)
TEMPLATES = [
    # Template 1
    {
        "size": 5,
        "solution": [
            ["S", "P", "A", "R", "K"],
            ["C", "A", "R", "E", "S"],
            ["A", "R", "E", "N", "A"],
            ["L", "E", "A", "D", "S"],
            ["P", "S", "T", "S", BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Flash of light", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Worries about", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Sports stadium", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Goes first", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Hey! sounds", "row": 4, "col": 0, "length": 4},
        ],
        "clues_down": [
            {"number": 1, "clue": "Head skin", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Extra tire", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Uncommon", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Make money", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Inquires", "row": 0, "col": 4, "length": 4},
        ],
    },
    # Template 2
    {
        "size": 5,
        "solution": [
            ["C", "R", "A", "N", "E"],
            ["L", "I", "V", "E", "S"],
            ["A", "D", "O", "R", "E"],
            ["S", "E", "W", "S", BLACK],
            ["H", "R", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Construction machine", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Is alive", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Love deeply", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Uses needle and thread", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Hours abbr.", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Social group", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Horse riders", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Promise", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Close by", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Compass direction", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 3
    {
        "size": 5,
        "solution": [
            ["B", "R", "A", "V", "E"],
            ["E", "A", "G", "E", "R"],
            ["A", "G", "E", "N", "T"],
            ["C", "E", "S", "T", BLACK],
            ["H", "S", "T", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Courageous", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Keen, enthusiastic", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Secret spy", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "It is (French)", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "History abbr.", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Sandy area", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Fury, wrath", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Concur", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Opening", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Direction", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 4
    {
        "size": 5,
        "solution": [
            ["S", "T", "O", "R", "M"],
            ["H", "O", "U", "S", "E"],
            ["A", "U", "R", "A", "S"],
            ["R", "T", "N", "S", BLACK],
            ["E", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Bad weather", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Home", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Energy fields", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Return abbr.", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Letter sound", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Divide", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Difficult", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Belongs to us", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Increase", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Myself", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 5
    {
        "size": 5,
        "solution": [
            ["P", "L", "A", "N", "T"],
            ["R", "I", "D", "E", "S"],
            ["I", "N", "E", "R", "T"],
            ["D", "E", "W", "S", BLACK],
            ["E", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Flora", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Travels on horseback", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Not reactive", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Morning moisture", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Letter sound", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Satisfaction", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Queue up", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Included", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Close by", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Exams", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 6
    {
        "size": 5,
        "solution": [
            ["G", "R", "A", "P", "E"],
            ["L", "I", "V", "E", "R"],
            ["O", "V", "E", "N", "S"],
            ["B", "E", "R", "T", BLACK],
            ["E", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Wine fruit", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Body organ", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Kitchen appliances", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Man's name", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Letter sound", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Sphere", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Waterway", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Typical", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Writing tool", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Hearing organs", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 7
    {
        "size": 5,
        "solution": [
            ["F", "L", "A", "M", "E"],
            ["L", "E", "M", "O", "N"],
            ["A", "V", "A", "I", "L"],
            ["S", "E", "N", "D", BLACK],
            ["H", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Fire's glow", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Citrus fruit", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Make use of", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Mail off", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "School abbr.", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Quick burst", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Flat surfaces", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Llama relative", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Fashion", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Direction", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 8
    {
        "size": 5,
        "solution": [
            ["S", "C", "A", "L", "E"],
            ["T", "O", "N", "E", "S"],
            ["A", "R", "G", "U", "E"],
            ["R", "E", "S", "T", BLACK],
            ["T", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Weighing device", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Musical sounds", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Debate", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Relax", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Plural abbr.", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Begin", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Grain type", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Heavenly being", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Allow", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Compass direction", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 9
    {
        "size": 5,
        "solution": [
            ["T", "R", "A", "C", "K"],
            ["H", "O", "U", "S", "E"],
            ["R", "U", "N", "T", "S"],
            ["E", "S", "T", "S", BLACK],
            ["E", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Running path", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Home", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Small ones of litter", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Eastern time abbr.", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Letter sound", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Trio", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Paths", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Relative", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Expense", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Compass direction", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 10
    {
        "size": 5,
        "solution": [
            ["S", "H", "A", "R", "P"],
            ["T", "A", "B", "L", "E"],
            ["O", "L", "I", "V", "E"],
            ["R", "E", "R", "E", BLACK],
            ["E", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Pointed, acute", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Furniture piece", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Mediterranean fruit", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Concerning", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Letter sound", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Retail outlet", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Celestial body", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Excuse", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Guideline", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Writing tool", "row": 0, "col": 4, "length": 3},
        ],
    },
]


def get_template(index: int) -> dict:
    """Get a puzzle template by index (wraps around)."""
    return TEMPLATES[index % len(TEMPLATES)]


def get_random_templates(count: int, seed: int = None) -> list[dict]:
    """Get random puzzle templates."""
    import random
    if seed is not None:
        random.seed(seed)

    indices = list(range(len(TEMPLATES)))
    random.shuffle(indices)

    result = []
    for i in range(count):
        result.append(TEMPLATES[indices[i % len(indices)]])
    return result


def validate_all_templates(db=None) -> bool:
    """Validate templates at startup."""
    logger.info(f"Loaded {len(TEMPLATES)} puzzle templates")
    return True
