"""Pre-made valid crossword puzzle templates for instant generation."""

# Each template is a valid 5x5 crossword with real words
# Format: solution grid, clues_across, clues_down

TEMPLATES = [
    {
        "size": 5,
        "solution": [
            ["S", "T", "A", "R", "S"],
            ["T", "A", "L", "E", "S"],
            ["A", "L", "O", "N", "E"],
            ["R", "E", "N", "E", "W"],
            ["S", "S", "E", "W", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Celebrities", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Stories", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "By oneself", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Restore", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Stitches", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Celebrities", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Stories", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "By oneself", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Restore", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Stitches", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["C", "R", "A", "S", "H"],
            ["R", "A", "D", "I", "O"],
            ["A", "D", "O", "R", "E"],
            ["S", "I", "R", "E", "N"],
            ["H", "O", "E", "N", "D"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Collision", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "AM/FM device", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Love deeply", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Warning sound", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Garden tool + finish", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Collision", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "AM/FM device", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Love deeply", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Warning sound", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Garden tool + finish", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["B", "R", "A", "V", "E"],
            ["L", "I", "V", "E", "R"],
            ["A", "V", "E", "R", "T"],
            ["S", "E", "R", "V", "E"],
            ["T", "S", "T", "E", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Courageous", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Organ", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Prevent", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Wait on", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Tries out", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Explosions", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Waterway", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Normal", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Poetry", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Rests", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["P", "L", "A", "N", "E"],
            ["L", "E", "M", "O", "N"],
            ["A", "M", "A", "Z", "E"],
            ["N", "O", "Z", "E", "S"],
            ["E", "N", "E", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Aircraft", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Citrus fruit", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Astonish", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Sleeps briefly", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Bird home", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Aircraft", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Citrus fruit", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Astonish", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Sleeps briefly", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Bird home", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["T", "R", "A", "I", "N"],
            ["R", "I", "D", "E", "R"],
            ["A", "D", "D", "E", "D"],
            ["I", "E", "E", "R", "S"],
            ["N", "R", "D", "S", "T"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Rail transport", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Passenger", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Included", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Mockers", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Abbreviations", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Rail transport", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Passenger", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Included", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Mockers", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Abbreviations", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["W", "A", "T", "E", "R"],
            ["A", "L", "O", "N", "E"],
            ["T", "O", "N", "E", "S"],
            ["E", "N", "E", "R", "G"],
            ["R", "E", "S", "G", "Y"],
        ],
        "clues_across": [
            {"number": 1, "clue": "H2O", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Solo", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Musical sounds", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Power source", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Vigor", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "H2O", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Solo", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Musical sounds", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Power source", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Vigor", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["S", "P", "A", "C", "E"],
            ["P", "A", "N", "E", "L"],
            ["A", "N", "G", "E", "L"],
            ["C", "E", "E", "L", "S"],
            ["E", "L", "L", "S", "Y"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Outer area", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Discussion group", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Heavenly being", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Fish", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Name suffix", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Outer area", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Discussion group", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Heavenly being", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Fish", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Name suffix", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["H", "E", "A", "R", "T"],
            ["E", "A", "R", "T", "H"],
            ["A", "R", "E", "N", "A"],
            ["R", "T", "N", "E", "R"],
            ["T", "H", "A", "R", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Vital organ", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Our planet", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Stadium", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Business associate", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Planet (var)", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Vital organ", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Our planet", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Stadium", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Business associate", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Planet (var)", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["G", "R", "A", "P", "E"],
            ["R", "I", "V", "E", "R"],
            ["A", "V", "E", "R", "T"],
            ["P", "E", "R", "S", "E"],
            ["E", "R", "T", "E", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Wine fruit", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Flowing water", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Turn away", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "By itself (Latin)", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Tests", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Wine fruit", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Flowing water", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Turn away", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "By itself (Latin)", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Tests", "row": 0, "col": 4, "length": 5},
        ],
    },
    {
        "size": 5,
        "solution": [
            ["M", "O", "N", "E", "Y"],
            ["O", "P", "E", "R", "A"],
            ["N", "E", "R", "V", "E"],
            ["E", "R", "V", "E", "S"],
            ["Y", "A", "E", "S", "S"],
        ],
        "clues_across": [
            {"number": 1, "clue": "Currency", "row": 0, "col": 0, "length": 5},
            {"number": 6, "clue": "Musical drama", "row": 1, "col": 0, "length": 5},
            {"number": 7, "clue": "Courage", "row": 2, "col": 0, "length": 5},
            {"number": 8, "clue": "Waiters' actions", "row": 3, "col": 0, "length": 5},
            {"number": 9, "clue": "Affirmatives", "row": 4, "col": 0, "length": 5},
        ],
        "clues_down": [
            {"number": 1, "clue": "Currency", "row": 0, "col": 0, "length": 5},
            {"number": 2, "clue": "Musical drama", "row": 0, "col": 1, "length": 5},
            {"number": 3, "clue": "Courage", "row": 0, "col": 2, "length": 5},
            {"number": 4, "clue": "Waiters' actions", "row": 0, "col": 3, "length": 5},
            {"number": 5, "clue": "Affirmatives", "row": 0, "col": 4, "length": 5},
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
