"""Reminder CRUD endpoint tests."""

import pytest


REMINDER_PAYLOAD = {
    "title": "Test Reminder",
    "trigger_type": "scheduled",
    "trigger_config": {"datetime": "2026-06-01T10:00:00Z"},
    "priority": "high",
    "description": "A test reminder",
    "advance_notice": 15,
}


def _create_reminder(client, auth_headers, **overrides):
    """Helper to create a reminder and return response."""
    payload = {**REMINDER_PAYLOAD, **overrides}
    return client.post("/api/reminders", json=payload, headers=auth_headers)


class TestCreateReminder:
    def test_create_reminder(self, client, auth_headers):
        """Create a scheduled reminder."""
        resp = _create_reminder(client, auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Test Reminder"
        assert data["priority"] == "high"
        assert data["trigger_type"] == "scheduled"
        assert data["status"] == "active"
        assert data["advance_notice"] == 15
        assert "id" in data

    def test_create_minimal_reminder(self, client, auth_headers):
        """Create reminder with only required fields."""
        resp = client.post(
            "/api/reminders",
            json={
                "title": "Minimal",
                "trigger_type": "event",
                "trigger_config": {},
            },
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["priority"] == "medium"
        assert data["advance_notice"] == 0

    def test_create_reminder_unauthorized(self, client):
        """Creating reminder without auth fails."""
        resp = client.post("/api/reminders", json=REMINDER_PAYLOAD)
        assert resp.status_code == 422


class TestListReminders:
    def test_list_reminders(self, client, auth_headers):
        """List returns created reminders."""
        _create_reminder(client, auth_headers, title="First")
        _create_reminder(client, auth_headers, title="Second")
        resp = client.get("/api/reminders", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_list_reminders_empty(self, client, auth_headers):
        """Empty list when no reminders exist."""
        resp = client.get("/api/reminders", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["items"] == []

    def test_filter_by_category(self, client, auth_headers, db_session):
        """Filter reminders by category_id."""
        from app.models.category import Category
        from app.models.user import User

        user = db_session.query(User).filter(User.device_id == "test-device-001").first()
        cat = Category(user_id=user.id, name="Work")
        db_session.add(cat)
        db_session.commit()
        db_session.refresh(cat)

        _create_reminder(client, auth_headers, category_id=cat.id, title="Work task")
        _create_reminder(client, auth_headers, title="No category")

        resp = client.get(
            f"/api/reminders?category_id={cat.id}", headers=auth_headers
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Work task"

    def test_filter_by_status(self, client, auth_headers):
        """Filter reminders by status."""
        _create_reminder(client, auth_headers, title="Active task")
        resp = _create_reminder(client, auth_headers, title="Paused task")

        reminder_id = resp.json()["id"]
        client.post(
            f"/api/reminders/{reminder_id}/pause", headers=auth_headers
        )

        resp = client.get("/api/reminders?status=paused", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["status"] == "paused"

    def test_search_reminders(self, client, auth_headers):
        """Search reminders by title substring."""
        _create_reminder(client, auth_headers, title="Buy groceries")
        _create_reminder(client, auth_headers, title="Meeting notes")

        resp = client.get("/api/reminders?search=groceries", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Buy groceries"


class TestUpdateReminder:
    def test_update_reminder(self, client, auth_headers):
        """Update reminder fields."""
        create_resp = _create_reminder(client, auth_headers)
        reminder_id = create_resp.json()["id"]

        resp = client.put(
            f"/api/reminders/{reminder_id}",
            json={"title": "Updated Title", "priority": "low"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Updated Title"
        assert data["priority"] == "low"
        assert data["trigger_type"] == "scheduled"

    def test_update_nonexistent_reminder(self, client, auth_headers):
        """Updating non-existent reminder returns 404."""
        resp = client.put(
            "/api/reminders/nonexistent-id",
            json={"title": "X"},
            headers=auth_headers,
        )
        assert resp.status_code == 404


class TestDeleteReminder:
    def test_delete_reminder(self, client, auth_headers):
        """Delete removes the reminder."""
        create_resp = _create_reminder(client, auth_headers)
        reminder_id = create_resp.json()["id"]

        del_resp = client.delete(
            f"/api/reminders/{reminder_id}", headers=auth_headers
        )
        assert del_resp.status_code == 200
        assert del_resp.json() == {"ok": True}

        get_resp = client.get(
            f"/api/reminders/{reminder_id}", headers=auth_headers
        )
        assert get_resp.status_code == 404

    def test_delete_nonexistent_reminder(self, client, auth_headers):
        """Deleting non-existent reminder returns 404."""
        resp = client.delete(
            "/api/reminders/nonexistent-id", headers=auth_headers
        )
        assert resp.status_code == 404


class TestPauseResume:
    def test_pause_resume(self, client, auth_headers):
        """Pause then resume a reminder."""
        create_resp = _create_reminder(client, auth_headers)
        reminder_id = create_resp.json()["id"]

        pause_resp = client.post(
            f"/api/reminders/{reminder_id}/pause", headers=auth_headers
        )
        assert pause_resp.status_code == 200

        get_resp = client.get(
            f"/api/reminders/{reminder_id}", headers=auth_headers
        )
        assert get_resp.json()["status"] == "paused"

        resume_resp = client.post(
            f"/api/reminders/{reminder_id}/resume", headers=auth_headers
        )
        assert resume_resp.status_code == 200

        get_resp = client.get(
            f"/api/reminders/{reminder_id}", headers=auth_headers
        )
        assert get_resp.json()["status"] == "active"
