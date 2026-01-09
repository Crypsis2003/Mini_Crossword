"""Crossword puzzle generator using constraint satisfaction with backtracking."""

import random
import logging
from typing import Optional
from collections import deque

logger = logging.getLogger(__name__)


class CrosswordGrid:
    """Represents a crossword grid with black squares and slots."""

    BLACK = "."
    EMPTY = " "

    def __init__(self, size: int):
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.slots: list[dict] = []  # Word slots (across and down)

    def set_black(self, row: int, col: int) -> None:
        """Set a cell as black square."""
        self.grid[row][col] = self.BLACK

    def is_black(self, row: int, col: int) -> bool:
        """Check if cell is black."""
        return self.grid[row][col] == self.BLACK

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= row < self.size and 0 <= col < self.size

    def get_white_cells(self) -> list[tuple[int, int]]:
        """Get all white (non-black) cell positions."""
        cells = []
        for r in range(self.size):
            for c in range(self.size):
                if not self.is_black(r, c):
                    cells.append((r, c))
        return cells

    def is_connected(self) -> bool:
        """Check if all white cells are connected (no isolated regions)."""
        white_cells = self.get_white_cells()
        if not white_cells:
            return False

        # BFS from first white cell
        visited = set()
        queue = deque([white_cells[0]])
        visited.add(white_cells[0])

        while queue:
            r, c = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in white_cells and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return len(visited) == len(white_cells)

    def extract_slots(self) -> list[dict]:
        """Extract all word slots (across and down) from the grid."""
        slots = []
        clue_num = 1

        for r in range(self.size):
            for c in range(self.size):
                if self.is_black(r, c):
                    continue

                starts_across = (c == 0 or self.is_black(r, c - 1)) and \
                                (c + 1 < self.size and not self.is_black(r, c + 1))
                starts_down = (r == 0 or self.is_black(r - 1, c)) and \
                              (r + 1 < self.size and not self.is_black(r + 1, c))

                if starts_across or starts_down:
                    if starts_across:
                        length = self._get_slot_length(r, c, 0, 1)
                        if length >= 2:
                            slots.append({
                                "number": clue_num,
                                "direction": "across",
                                "row": r,
                                "col": c,
                                "length": length,
                                "cells": [(r, c + i) for i in range(length)],
                            })

                    if starts_down:
                        length = self._get_slot_length(r, c, 1, 0)
                        if length >= 2:
                            slots.append({
                                "number": clue_num,
                                "direction": "down",
                                "row": r,
                                "col": c,
                                "length": length,
                                "cells": [(r + i, c) for i in range(length)],
                            })

                    if starts_across or starts_down:
                        clue_num += 1

        self.slots = slots
        return slots

    def _get_slot_length(self, row: int, col: int, dr: int, dc: int) -> int:
        """Get length of a word slot in given direction."""
        length = 0
        r, c = row, col
        while self.is_valid_position(r, c) and not self.is_black(r, c):
            length += 1
            r += dr
            c += dc
        return length

    def has_isolated_letters(self) -> bool:
        """Check if any white cell is only in slots of length 1."""
        self.extract_slots()
        cell_slot_count = {}

        for slot in self.slots:
            if slot["length"] >= 2:
                for cell in slot["cells"]:
                    cell_slot_count[cell] = cell_slot_count.get(cell, 0) + 1

        # Every white cell should be in at least one valid slot
        for cell in self.get_white_cells():
            if cell not in cell_slot_count:
                return True

        return False

    def is_valid_pattern(self) -> bool:
        """Check if grid pattern is valid for a crossword."""
        if not self.is_connected():
            return False
        if self.has_isolated_letters():
            return False

        # Check no 1-letter words
        self.extract_slots()
        for slot in self.slots:
            if slot["length"] < 2:
                return False

        return len(self.slots) >= 2  # Need at least some slots


class CrosswordFiller:
    """Fills a crossword grid using backtracking with constraint propagation."""

    def __init__(self, grid: CrosswordGrid, words_by_length: dict[int, list[str]]):
        self.grid = grid
        self.words_by_length = words_by_length
        self.solution = [[cell for cell in row] for row in grid.grid]
        self.used_words: set[str] = set()

    def fill(self, max_backtracks: int = 1000) -> bool:
        """
        Fill the grid with words using backtracking.

        Returns True if successful, False otherwise.
        """
        slots = self.grid.slots[:]
        # Sort by most constrained first (longest slots, then by intersections)
        slots.sort(key=lambda s: (-s["length"], -len(self._get_intersections(s))))

        self.backtrack_count = 0
        return self._backtrack(slots, 0, max_backtracks)

    def _backtrack(self, slots: list[dict], idx: int, max_backtracks: int) -> bool:
        """Recursive backtracking search."""
        if idx >= len(slots):
            return True  # All slots filled

        if self.backtrack_count >= max_backtracks:
            return False

        slot = slots[idx]
        candidates = self._get_candidates(slot)
        random.shuffle(candidates)  # Randomize for variety

        for word in candidates:
            if word in self.used_words:
                continue

            if self._try_place_word(slot, word):
                self.used_words.add(word)

                if self._backtrack(slots, idx + 1, max_backtracks):
                    return True

                # Backtrack
                self.backtrack_count += 1
                self._remove_word(slot, word)
                self.used_words.discard(word)

        return False

    def _get_candidates(self, slot: dict) -> list[str]:
        """Get candidate words that fit the slot's constraints."""
        length = slot["length"]
        if length not in self.words_by_length:
            return []

        candidates = []
        pattern = self._get_pattern(slot)

        for word in self.words_by_length[length]:
            if self._matches_pattern(word, pattern):
                candidates.append(word)

        return candidates

    def _get_pattern(self, slot: dict) -> list[Optional[str]]:
        """Get current letter constraints for a slot."""
        pattern = []
        for r, c in slot["cells"]:
            cell = self.solution[r][c]
            if cell == CrosswordGrid.EMPTY or cell == CrosswordGrid.BLACK:
                pattern.append(None)
            else:
                pattern.append(cell)
        return pattern

    def _matches_pattern(self, word: str, pattern: list[Optional[str]]) -> bool:
        """Check if word matches the pattern constraints."""
        if len(word) != len(pattern):
            return False
        for i, char in enumerate(pattern):
            if char is not None and word[i] != char:
                return False
        return True

    def _try_place_word(self, slot: dict, word: str) -> bool:
        """Try to place a word in the slot. Returns True if valid."""
        # Check all intersections before placing
        for i, (r, c) in enumerate(slot["cells"]):
            current = self.solution[r][c]
            if current != CrosswordGrid.EMPTY and current != word[i]:
                return False

        # Place the word
        for i, (r, c) in enumerate(slot["cells"]):
            self.solution[r][c] = word[i]

        return True

    def _remove_word(self, slot: dict, word: str) -> None:
        """Remove a word from the slot (for backtracking)."""
        # Only clear cells that aren't used by other filled slots
        for i, (r, c) in enumerate(slot["cells"]):
            # Check if any other slot uses this cell and is filled
            other_uses_cell = False
            for other_slot in self.grid.slots:
                if other_slot == slot:
                    continue
                if (r, c) in other_slot["cells"]:
                    # Check if other slot has a word
                    other_pattern = self._get_pattern(other_slot)
                    if all(p is not None for p in other_pattern):
                        other_uses_cell = True
                        break

            if not other_uses_cell:
                self.solution[r][c] = CrosswordGrid.EMPTY

    def _get_intersections(self, slot: dict) -> list[tuple[dict, int, int]]:
        """Get all slots that intersect with this slot."""
        intersections = []
        for other in self.grid.slots:
            if other == slot:
                continue
            for i, cell in enumerate(slot["cells"]):
                if cell in other["cells"]:
                    j = other["cells"].index(cell)
                    intersections.append((other, i, j))
        return intersections

    def get_solution(self) -> list[list[str]]:
        """Get the filled solution grid."""
        return self.solution


def generate_random_pattern(size: int, black_ratio: float = 0.15, max_attempts: int = 100) -> Optional[CrosswordGrid]:
    """
    Generate a random valid crossword pattern.

    Args:
        size: Grid size (5, 6, or 7)
        black_ratio: Target ratio of black squares (0.1-0.2 typical)
        max_attempts: Maximum generation attempts

    Returns:
        Valid CrosswordGrid or None if failed
    """
    target_blacks = int(size * size * black_ratio)

    for attempt in range(max_attempts):
        grid = CrosswordGrid(size)

        # Randomly place black squares
        num_blacks = random.randint(max(0, target_blacks - 2), target_blacks + 2)
        positions = [(r, c) for r in range(size) for c in range(size)]
        random.shuffle(positions)

        blacks_placed = 0
        for r, c in positions:
            if blacks_placed >= num_blacks:
                break

            # Try placing black square
            grid.set_black(r, c)

            # Check if still valid
            if not grid.is_connected():
                grid.grid[r][c] = CrosswordGrid.EMPTY  # Undo
            else:
                blacks_placed += 1

        # Validate final pattern
        if grid.is_valid_pattern():
            grid.extract_slots()
            logger.debug(f"Generated valid pattern on attempt {attempt + 1}: {len(grid.slots)} slots")
            return grid

    logger.warning(f"Failed to generate valid pattern after {max_attempts} attempts")
    return None


def generate_puzzle(size: int, words_by_length: dict[int, list[str]], max_attempts: int = 50) -> Optional[dict]:
    """
    Generate a complete crossword puzzle.

    Args:
        size: Grid size (5, 6, or 7)
        words_by_length: Dictionary mapping length -> list of words
        max_attempts: Maximum attempts to generate a valid puzzle

    Returns:
        Puzzle dict with grid, solution, clues, or None if failed
    """
    for attempt in range(max_attempts):
        # Generate a random valid pattern
        grid = generate_random_pattern(size, black_ratio=0.12)
        if not grid:
            continue

        # Try to fill it with words
        filler = CrosswordFiller(grid, words_by_length)
        if filler.fill(max_backtracks=2000):
            solution = filler.get_solution()

            # Build puzzle dict
            # Grid for play (black squares visible, letters hidden)
            play_grid = [
                [CrosswordGrid.BLACK if cell == CrosswordGrid.BLACK else " " for cell in row]
                for row in solution
            ]

            # Generate clues
            clues_across = []
            clues_down = []

            for slot in grid.slots:
                word = "".join(solution[r][c] for r, c in slot["cells"])
                clue_entry = {
                    "number": slot["number"],
                    "clue": f"{slot['direction'].capitalize()} {slot['number']}",  # Placeholder
                    "length": slot["length"],
                    "row": slot["row"],
                    "col": slot["col"],
                }

                if slot["direction"] == "across":
                    clues_across.append(clue_entry)
                else:
                    clues_down.append(clue_entry)

            logger.debug(f"Generated puzzle on attempt {attempt + 1}")
            return {
                "size": size,
                "grid": play_grid,
                "solution": solution,
                "clues_across": sorted(clues_across, key=lambda x: x["number"]),
                "clues_down": sorted(clues_down, key=lambda x: x["number"]),
                "slots": grid.slots,
            }

    logger.warning(f"Failed to generate puzzle after {max_attempts} attempts")
    return None
