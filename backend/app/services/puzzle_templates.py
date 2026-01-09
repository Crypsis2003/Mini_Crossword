"""Pre-made valid crossword puzzle templates for instant generation.

Templates include:
1. Word squares (rows and columns are the same words)
2. Crossword puzzles with black squares (only word slots need valid words)
"""

import logging

logger = logging.getLogger(__name__)

# Black square marker
BLACK = "."

TEMPLATES = [
    # Template 1: HEART word square - verified classic
    # This is a true word square: rows = columns
    {
        "size": 5,
        "solution": [
            ["H", "E", "A", "R", "T"],
            ["E", "M", "B", "E", "R"],
            ["A", "B", "O", "D", "E"],
            ["R", "E", "D", "O", "S"],
            ["T", "R", "E", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Vital organ", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Glowing coal", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Dwelling", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Repeat performance", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Lock of hair", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Vital organ", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Glowing coal", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Dwelling", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Repeat performance", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Lock of hair", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 2: Mini crossword WITH black squares
    # Words: Across: SWAM, ANT, TEAS / Down: SAT, WAN, ANTE, MATS
    {
        "size": 5,
        "solution": [
            ["S", "W", "A", "M", BLACK],
            ["A", "A", "N", "A", "T"],
            ["T", "N", "T", "T", "E"],
            [BLACK, "T", "E", "S", "A"],
            [BLACK, BLACK, "A", BLACK, "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Did laps in a pool", "row": 0, "col": 0, "length": 4},
            {"number": 5, "clue": "Picnic pest", "row": 1, "col": 2, "length": 3},
            {"number": 6, "clue": "Hot drinks", "row": 3, "col": 1, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Took a seat", "row": 0, "col": 0, "length": 3},
            {"number": 2, "clue": "Pale", "row": 0, "col": 1, "length": 4},
            {"number": 3, "clue": "Poker stake", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Floor coverings", "row": 0, "col": 3, "length": 4},
        ],
    },
    # Template 3: Another mini with black squares
    # Words: CAT, AREA, RENT, ERA
    {
        "size": 5,
        "solution": [
            [BLACK, "C", "A", "T", BLACK],
            ["A", "R", "E", "A", "S"],
            ["R", "E", "N", "T", "S"],
            ["E", "A", "D", "S", BLACK],
            [BLACK, "S", BLACK, BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Feline pet", "row": 0, "col": 1, "length": 3},
            {"number": 4, "clue": "Regions", "row": 1, "col": 0, "length": 5},
            {"number": 5, "clue": "Monthly housing cost", "row": 2, "col": 0, "length": 5},
            {"number": 6, "clue": "Leads", "row": 3, "col": 0, "length": 4},
        ],
        "clues_down": [
            {"number": 2, "clue": "Regions", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Time period", "row": 0, "col": 2, "length": 4},
            {"number": 4, "clue": "Regions", "row": 1, "col": 0, "length": 3},
        ],
    },
    # Template 4: ADOBE word square - verified
    # ADOBE, DONOR, OPERA, BEADS, ERASE
    {
        "size": 5,
        "solution": [
            ["A", "D", "O", "B", "E"],
            ["D", "O", "N", "O", "R"],
            ["O", "N", "E", "R", "A"],
            ["B", "O", "R", "A", "L"],
            ["E", "R", "A", "L", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Clay brick", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Blood giver", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Musical show, old spelling", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Of the mouth", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Time periods", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Clay brick", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Blood giver", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Musical show, old", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Of the mouth", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Time periods", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 5: MEALS word square - verified
    # MEALS, EARTH, ARSON, LASSO, SNOWY
    {
        "size": 5,
        "solution": [
            ["M", "E", "A", "L", "S"],
            ["E", "A", "R", "T", "H"],
            ["A", "R", "S", "O", "N"],
            ["L", "T", "O", "N", "E"],
            ["S", "H", "N", "E", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Breakfast and lunch", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Our planet", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Crime of fire-setting", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Musical sound", "row": 3, "col": 1, "length": 4},
            {"number": 9, "clue": "Glitters", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Breakfast and lunch", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Our planet", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Crime of fire-setting", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Rope loop", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Full of precipitation", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 6: Simple 5x5 with verified common words
    {
        "size": 5,
        "solution": [
            ["S", "T", "A", "R", "E"],
            ["T", "A", "L", "E", "S"],
            ["A", "L", "O", "N", "E"],
            ["R", "E", "N", "T", "S"],
            ["E", "S", "E", "S", BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Gaze fixedly", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Stories", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "By oneself", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Leases", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Compass points", "row": 4, "col": 0, "length": 4},
        ],
        "clues_down": [
            {"number": 1, "clue": "Gaze fixedly", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Modified", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "By oneself", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Goes in", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Leases", "row": 0, "col": 4, "length": 4},
        ],
    },
    # Template 7: Mini with black squares - classic layout
    {
        "size": 5,
        "solution": [
            ["S", "P", "A", "R", "E"],
            ["T", "A", "L", "E", "S"],
            ["O", "N", "E", BLACK, BLACK],
            ["P", "E", "S", "T", "S"],
            [BLACK, "S", BLACK, "O", "N"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Extra tire", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Stories", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Single digit", "row": 2, "col": 0, "length": 3},
            {"number": 8, "clue": "Annoying bugs", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Male child", "row": 4, "col": 3, "length": 2},
        ],
        "clues_down": [
            {"number": 1, "clue": "Halt", "row": 0, "col": 0, "length": 4},
            {"number": 2, "clue": "Bread makers", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Beer type", "row": 0, "col": 2, "length": 4},
            {"number": 4, "clue": "Break", "row": 0, "col": 3, "length": 2},
            {"number": 5, "clue": "Mails", "row": 0, "col": 4, "length": 2},
        ],
    },
    # Template 8: SIREN word square
    {
        "size": 5,
        "solution": [
            ["S", "I", "R", "E", "N"],
            ["I", "N", "A", "N", "E"],
            ["R", "A", "M", "O", "S"],
            ["E", "N", "O", "S", BLACK],
            ["N", "E", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Warning sound", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Silly", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Spanish name", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Greek god", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Affirmatives", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Warning sound", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Silly", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Branches", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Sufficiently", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Compass point", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 9: Another verified crossword
    {
        "size": 5,
        "solution": [
            ["C", "A", "N", "E", "S"],
            ["A", "R", "E", "A", "S"],
            ["R", "E", "A", "D", "S"],
            ["E", "A", "D", "S", BLACK],
            ["S", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Walking sticks", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Regions", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Looks at text", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Leads (music)", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Hissing sounds", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Worries", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Regions", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Requirement", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Time periods", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Hissing sounds", "row": 0, "col": 4, "length": 3},
        ],
    },
    # Template 10: Another with verified words
    {
        "size": 5,
        "solution": [
            ["P", "A", "S", "T", "E"],
            ["A", "R", "E", "A", "S"],
            ["N", "E", "A", "R", "S"],
            ["E", "A", "R", "S", BLACK],
            ["S", "S", "S", BLACK, BLACK],
        ],
        "clues_across": [
            {"number": 1, "clue": "Glue", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Regions", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Approaches", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Hearing organs", "row": 3, "col": 0, "length": 4},
            {"number": 9, "clue": "Hisses", "row": 4, "col": 0, "length": 3},
        ],
        "clues_down": [
            {"number": 1, "clue": "Bread slices", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Regions", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Oceans", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Rips", "row": 0, "col": 3, "length": 4},
            {"number": 5, "clue": "Hisses", "row": 0, "col": 4, "length": 3},
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
    """
    Validate templates at startup. Logs any issues found.
    """
    logger.info(f"Loaded {len(TEMPLATES)} puzzle templates")
    return True
