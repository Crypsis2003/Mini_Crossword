"""Tests for puzzle endpoints."""

import pytest


class TestGetPuzzle:
    """Tests for getting puzzles."""

    def test_get_today_puzzle(self, client, sample_puzzle):
        """Test getting today's puzzle."""
        response = client.get("/api/puzzles/today")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Puzzle"
        assert data["size"] == 5
        assert "grid" in data
        assert "clues_across" in data
        assert "clues_down" in data
        # Solution should not be included
        assert "solution" not in data

    def test_get_puzzle_by_id(self, client, sample_puzzle):
        """Test getting puzzle by ID."""
        response = client.get(f"/api/puzzles/{sample_puzzle.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_puzzle.id
        assert data["title"] == "Test Puzzle"

    def test_get_puzzle_not_found(self, client):
        """Test getting nonexistent puzzle."""
        response = client.get("/api/puzzles/99999")
        assert response.status_code == 404

    def test_get_today_no_puzzle(self, client, db):
        """Test getting today's puzzle when none exists."""
        response = client.get("/api/puzzles/today")
        assert response.status_code == 404


class TestCheckPuzzle:
    """Tests for checking puzzle solutions."""

    def test_check_correct_solution(self, client, sample_puzzle):
        """Test checking a correct solution."""
        correct_grid = [
            ["H", "E", "L", "L", "O"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]
        response = client.post(
            f"/api/puzzles/{sample_puzzle.id}/check",
            json=correct_grid,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_correct"] is True
        assert len(data["incorrect_cells"]) == 0

    def test_check_incorrect_solution(self, client, sample_puzzle):
        """Test checking an incorrect solution."""
        incorrect_grid = [
            ["H", "E", "L", "L", "X"],  # Wrong last letter
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]
        response = client.post(
            f"/api/puzzles/{sample_puzzle.id}/check",
            json=incorrect_grid,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_correct"] is False
        assert len(data["incorrect_cells"]) == 1
        assert [0, 4] in data["incorrect_cells"]

    def test_check_partial_solution(self, client, sample_puzzle):
        """Test checking a partial solution."""
        partial_grid = [
            ["H", "E", "L", "L", ""],  # Missing last letter
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]
        response = client.post(
            f"/api/puzzles/{sample_puzzle.id}/check",
            json=partial_grid,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_correct"] is False


class TestSolvePuzzle:
    """Tests for submitting puzzle solves."""

    def test_solve_puzzle_success(self, client, sample_puzzle, sample_user, auth_headers):
        """Test submitting a correct solve."""
        correct_grid = [
            ["H", "E", "L", "L", "O"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]
        response = client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 60000,  # 1 minute
                "grid": correct_grid,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["time_ms"] == 60000
        assert "rank" in data
        assert "share_text" in data

    def test_solve_puzzle_incorrect(self, client, sample_puzzle, sample_user, auth_headers):
        """Test submitting an incorrect solve."""
        incorrect_grid = [
            ["H", "E", "L", "L", "X"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]
        response = client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 60000,
                "grid": incorrect_grid,
            },
        )
        assert response.status_code == 400
        assert "incorrect" in response.json()["detail"].lower()

    def test_solve_puzzle_unauthorized(self, client, sample_puzzle):
        """Test submitting solve without auth."""
        response = client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 60000,
                "grid": [["A"] * 5] * 5,
            },
        )
        assert response.status_code == 401

    def test_get_my_solve(self, client, sample_puzzle, sample_user, auth_headers):
        """Test getting user's solve for a puzzle."""
        # First solve the puzzle
        correct_grid = [
            ["H", "E", "L", "L", "O"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]
        client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 60000,
                "grid": correct_grid,
            },
        )

        # Get the solve
        response = client.get(
            f"/api/puzzles/{sample_puzzle.id}/my-solve",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["solved"] is True
        assert data["time_ms"] == 60000
