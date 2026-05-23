"""Authentication endpoint tests."""

import pytest


class TestVerifyAuth:
    """POST /api/auth/verify"""

    def test_verify_new_user(self, client):
        """New device registration creates a user."""
        resp = client.post(
            "/api/auth/verify",
            json={"device_id": "new-device-999", "api_provider": "deepseek"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["device_id"] == "new-device-999"
        assert data["api_provider"] == "deepseek"
        assert "id" in data
        assert "created_at" in data

    def test_verify_existing_user(self, client, test_user):
        """Existing device returns the same user and updates api_provider."""
        resp = client.post(
            "/api/auth/verify",
            json={
                "device_id": test_user.device_id,
                "api_provider": "claude",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == test_user.id
        assert data["api_provider"] == "claude"

    def test_verify_without_device_id(self, client):
        """Missing device_id returns 422 (validation error)."""
        resp = client.post("/api/auth/verify", json={})
        assert resp.status_code == 422

    def test_verify_empty_device_id(self, client):
        """Empty device_id returns 400."""
        resp = client.post(
            "/api/auth/verify",
            json={"device_id": ""},
        )
        assert resp.status_code == 400


class TestGetProfile:
    """GET /api/auth/profile"""

    def test_get_profile(self, client, auth_headers):
        """Authenticated request returns user profile."""
        resp = client.get("/api/auth/profile", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["device_id"] == "test-device-001"
        assert "id" in data

    def test_unauthorized_access(self, client):
        """Missing device_id header returns 422."""
        resp = client.get("/api/auth/profile")
        assert resp.status_code == 422

    def test_unknown_device_returns_404(self, client):
        """Unknown device_id returns 404."""
        resp = client.get(
            "/api/auth/profile",
            headers={"X-Device-Id": "nonexistent-device"},
        )
        assert resp.status_code == 404
