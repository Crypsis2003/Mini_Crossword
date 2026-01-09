"""Tests for authentication endpoints."""

import pytest


class TestRegister:
    """Tests for user registration."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "hashed_password" not in data

    def test_register_duplicate_username(self, client, sample_user):
        """Test registration with existing username."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "different@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, sample_user):
        """Test registration with existing email."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "differentuser",
                "email": "test@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "invalid-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    def test_register_short_password(self, client):
        """Test registration with short password."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "short",
            },
        )
        assert response.status_code == 422


class TestLogin:
    """Tests for user login."""

    def test_login_success(self, client, sample_user):
        """Test successful login."""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, sample_user):
        """Test login with wrong password."""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password123"},
        )
        assert response.status_code == 401


class TestAuth:
    """Tests for authenticated endpoints."""

    def test_get_me(self, client, sample_user, auth_headers):
        """Test getting current user."""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_me_unauthorized(self, client):
        """Test getting current user without auth."""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_get_profile(self, client, sample_user, auth_headers):
        """Test getting user profile with stats."""
        response = client.get("/api/auth/profile", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert "total_solves" in data
        assert "friends_count" in data

    def test_logout(self, client, sample_user, auth_headers):
        """Test logout."""
        response = client.post("/api/auth/logout", headers=auth_headers)
        assert response.status_code == 200
        assert "Successfully logged out" in response.json()["message"]
