"""Tests for leaderboard endpoints."""

import pytest
from app.models.solve import Solve


class TestLeaderboard:
    """Tests for leaderboard functionality."""

    def test_get_today_leaderboard_empty(self, client, sample_puzzle):
        """Test getting leaderboard with no solves."""
        response = client.get("/api/leaderboard/today")
        assert response.status_code == 200
        data = response.json()
        assert data["puzzle_id"] == sample_puzzle.id
        assert len(data["entries"]) == 0

    def test_leaderboard_ordering(self, client, db, sample_puzzle, sample_user, sample_user2, auth_headers, auth_headers2):
        """Test that leaderboard is ordered by time (fastest first)."""
        # Correct solution
        correct_grid = [
            ["H", "E", "L", "L", "O"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]

        # User 1 solves in 120 seconds
        client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 120000,
                "grid": correct_grid,
            },
        )

        # User 2 solves in 60 seconds (faster)
        client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers2,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 60000,
                "grid": correct_grid,
            },
        )

        # Get leaderboard
        response = client.get("/api/leaderboard/today")
        assert response.status_code == 200
        data = response.json()

        assert len(data["entries"]) == 2

        # Verify ordering - fastest first
        assert data["entries"][0]["time_ms"] == 60000
        assert data["entries"][0]["username"] == "testuser2"
        assert data["entries"][0]["rank"] == 1

        assert data["entries"][1]["time_ms"] == 120000
        assert data["entries"][1]["username"] == "testuser"
        assert data["entries"][1]["rank"] == 2

    def test_leaderboard_current_user_flag(self, client, db, sample_puzzle, sample_user, auth_headers):
        """Test that current user is flagged in leaderboard."""
        correct_grid = [
            ["H", "E", "L", "L", "O"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]

        # Solve the puzzle
        client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 60000,
                "grid": correct_grid,
            },
        )

        # Get leaderboard with auth
        response = client.get("/api/leaderboard/today", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        assert len(data["entries"]) == 1
        assert data["entries"][0]["is_current_user"] is True

    def test_leaderboard_user_entry(self, client, db, sample_puzzle, sample_user, sample_user2, auth_headers, auth_headers2):
        """Test that user's entry is returned separately."""
        correct_grid = [
            ["H", "E", "L", "L", "O"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]

        # Both users solve
        client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 120000,
                "grid": correct_grid,
            },
        )
        client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers2,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 60000,
                "grid": correct_grid,
            },
        )

        # Get leaderboard as user 1
        response = client.get("/api/leaderboard/today", headers=auth_headers)
        data = response.json()

        assert data["user_entry"] is not None
        assert data["user_entry"]["username"] == "testuser"
        assert data["user_entry"]["rank"] == 2  # Second place

    def test_get_puzzle_leaderboard(self, client, db, sample_puzzle, sample_user, auth_headers):
        """Test getting leaderboard for a specific puzzle."""
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

        response = client.get(f"/api/leaderboard/puzzle/{sample_puzzle.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["puzzle_id"] == sample_puzzle.id
        assert len(data["entries"]) == 1

    def test_improved_time_updates_rank(self, client, db, sample_puzzle, sample_user, auth_headers):
        """Test that improving time updates the leaderboard."""
        correct_grid = [
            ["H", "E", "L", "L", "O"],
            ["A", ".", "I", ".", "N"],
            ["P", "E", "A", "C", "E"],
            ["P", ".", "R", ".", "S"],
            ["Y", "E", "S", "E", "S"],
        ]

        # First solve - 120 seconds
        client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 120000,
                "grid": correct_grid,
            },
        )

        # Second solve - 60 seconds (faster)
        response = client.post(
            f"/api/puzzles/{sample_puzzle.id}/solve",
            headers=auth_headers,
            json={
                "puzzle_id": sample_puzzle.id,
                "time_ms": 60000,
                "grid": correct_grid,
            },
        )
        data = response.json()
        assert data["is_new_record"] is True
        assert data["time_ms"] == 60000

        # Verify leaderboard shows improved time
        response = client.get("/api/leaderboard/today")
        data = response.json()
        assert data["entries"][0]["time_ms"] == 60000
