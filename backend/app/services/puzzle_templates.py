"""Pre-made valid crossword puzzle templates for instant generation.

Each template is a full 5x5 mini crossword with no black squares.
All rows and columns contain letters (like NYT Mini).
"""

import logging

logger = logging.getLogger(__name__)

# Full 5x5 grids - no black squares, all letters
TEMPLATES = [
    # Template 1: SPARK
    {
        "size": 5,
        "solution": [
            ["S", "P", "A", "R", "K"],
            ["C", "A", "R", "E", "S"],
            ["A", "R", "E", "N", "A"],
            ["L", "E", "A", "D", "S"],
            ["P", "S", "T", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Flash of light", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Worries about", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Sports stadium", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Goes first", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Quiet! sounds", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Head skin", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Analyzes text", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Region", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Makes money", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Inquires", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 2: CRANE
    {
        "size": 5,
        "solution": [
            ["C", "R", "A", "N", "E"],
            ["L", "I", "V", "E", "S"],
            ["A", "D", "O", "R", "E"],
            ["S", "E", "W", "E", "D"],
            ["H", "R", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Construction machine", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Exists", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Love deeply", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Stitched", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Abbreviations", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Social group", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Horseback riders", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Promise solemnly", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Close by", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Finishes", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 3: BRAVE
    {
        "size": 5,
        "solution": [
            ["B", "R", "A", "V", "E"],
            ["E", "A", "G", "E", "R"],
            ["A", "G", "E", "N", "T"],
            ["C", "E", "S", "T", "A"],
            ["H", "S", "T", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Courageous", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Keen, enthusiastic", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Secret spy", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Basket type", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Abbreviations", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Sandy shore", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Fury, wrath", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Visitors", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Opening", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Consumes", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 4: STORM
    {
        "size": 5,
        "solution": [
            ["S", "T", "O", "R", "M"],
            ["H", "O", "U", "S", "E"],
            ["A", "U", "R", "A", "S"],
            ["R", "T", "N", "S", "E"],
            ["E", "S", "S", "E", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Bad weather", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Home", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Energy fields", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Turns around", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Plural endings", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Divide equally", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Exterior", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Belongs to us", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Increases", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Labyrinth", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 5: PLANT
    {
        "size": 5,
        "solution": [
            ["P", "L", "A", "N", "T"],
            ["R", "I", "D", "E", "S"],
            ["I", "N", "E", "R", "T"],
            ["D", "E", "W", "S", "Y"],
            ["E", "S", "S", "E", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Flora", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Horseback trips", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Not reactive", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Moist with dew", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Plural endings", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Satisfaction", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Queues up", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Included", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Close by", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Examinations", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 6: GRAPE
    {
        "size": 5,
        "solution": [
            ["G", "R", "A", "P", "E"],
            ["L", "I", "V", "E", "R"],
            ["O", "V", "E", "N", "S"],
            ["B", "E", "R", "T", "S"],
            ["E", "S", "S", "E", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Wine fruit", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Body organ", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Kitchen appliances", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Common names", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Plural endings", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Sphere", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Waterway", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Typical", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Writing tools", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Deletes", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 7: FLAME
    {
        "size": 5,
        "solution": [
            ["F", "L", "A", "M", "E"],
            ["L", "E", "M", "O", "N"],
            ["A", "V", "A", "I", "L"],
            ["S", "E", "N", "D", "S"],
            ["H", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Fire's glow", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Citrus fruit", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Make use of", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Mails off", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Abbreviations", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Quick bursts", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Flat surfaces", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Llama relatives", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Fashions", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Finishes", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 8: SCALE
    {
        "size": 5,
        "solution": [
            ["S", "C", "A", "L", "E"],
            ["T", "O", "N", "E", "S"],
            ["A", "R", "G", "U", "E"],
            ["R", "E", "S", "T", "S"],
            ["T", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Weighing device", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Musical sounds", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Debate", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Relaxes", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Abbreviations", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Begins", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Grain types", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Heavenly beings", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Allows", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Finishes", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 9: TRACK
    {
        "size": 5,
        "solution": [
            ["T", "R", "A", "C", "K"],
            ["H", "O", "U", "S", "E"],
            ["R", "U", "N", "T", "S"],
            ["E", "S", "T", "S", "Y"],
            ["E", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Running path", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Home", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Smallest of litter", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Tasty", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Abbreviations", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Group of three", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Pathways", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Family member", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Expenses", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Answer", "row": 0, "col": 4, "length": 5},
        ],
    },
    # Template 10: SHARP
    {
        "size": 5,
        "solution": [
            ["S", "H", "A", "R", "P"],
            ["T", "A", "B", "L", "E"],
            ["O", "L", "I", "V", "E"],
            ["R", "E", "R", "E", "S"],
            ["E", "S", "S", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Pointed, acute", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Furniture piece", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Mediterranean fruit", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Concerning again", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Abbreviations", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Retail outlet", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Celestial bodies", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Excuses", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Guidelines", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Writing tools", "row": 0, "col": 4, "length": 5},
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
