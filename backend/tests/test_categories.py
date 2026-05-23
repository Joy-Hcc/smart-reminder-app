"""Category endpoint tests."""

import pytest


class TestCreateCategory:
    def test_create_category(self, client, auth_headers):
        """Create a top-level category."""
        resp = client.post(
            "/api/categories",
            json={"name": "Work", "icon": "briefcase"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Work"
        assert data["icon"] == "briefcase"
        assert data["parent_id"] is None
        assert data["sort_order"] == 0
        assert "id" in data

    def test_create_subcategory(self, client, auth_headers):
        """Create a child category under a parent."""
        parent_resp = client.post(
            "/api/categories",
            json={"name": "Work"},
            headers=auth_headers,
        )
        parent_id = parent_resp.json()["id"]

        child_resp = client.post(
            "/api/categories",
            json={"name": "Meetings", "parent_id": parent_id, "sort_order": 1},
            headers=auth_headers,
        )
        assert child_resp.status_code == 200
        data = child_resp.json()
        assert data["name"] == "Meetings"
        assert data["parent_id"] == parent_id
        assert data["sort_order"] == 1

    def test_create_category_unauthorized(self, client):
        """Creating category without auth fails."""
        resp = client.post("/api/categories", json={"name": "X"})
        assert resp.status_code == 422


class TestListCategories:
    def test_list_categories(self, client, auth_headers):
        """List returns top-level categories with children nested."""
        parent_resp = client.post(
            "/api/categories",
            json={"name": "Personal"},
            headers=auth_headers,
        )
        parent_id = parent_resp.json()["id"]

        client.post(
            "/api/categories",
            json={"name": "Health", "parent_id": parent_id},
            headers=auth_headers,
        )
        client.post(
            "/api/categories",
            json={"name": "Finance", "parent_id": parent_id},
            headers=auth_headers,
        )
        client.post(
            "/api/categories",
            json={"name": "Work"},
            headers=auth_headers,
        )

        resp = client.get("/api/categories", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2

        personal = next(c for c in data if c["name"] == "Personal")
        assert len(personal["children"]) == 2

    def test_list_categories_empty(self, client, auth_headers):
        """Empty list when no categories exist."""
        resp = client.get("/api/categories", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []


class TestUpdateCategory:
    def test_update_category(self, client, auth_headers):
        """Update category name and icon."""
        create_resp = client.post(
            "/api/categories",
            json={"name": "Old Name"},
            headers=auth_headers,
        )
        cat_id = create_resp.json()["id"]

        resp = client.put(
            f"/api/categories/{cat_id}",
            json={"name": "New Name", "icon": "star"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "New Name"
        assert data["icon"] == "star"

    def test_update_nonexistent_category(self, client, auth_headers):
        """Updating non-existent category returns 404."""
        resp = client.put(
            "/api/categories/nonexistent",
            json={"name": "X"},
            headers=auth_headers,
        )
        assert resp.status_code == 404


class TestDeleteCategory:
    def test_delete_category(self, client, auth_headers):
        """Delete removes the category."""
        create_resp = client.post(
            "/api/categories",
            json={"name": "To Delete"},
            headers=auth_headers,
        )
        cat_id = create_resp.json()["id"]

        del_resp = client.delete(
            f"/api/categories/{cat_id}", headers=auth_headers
        )
        assert del_resp.status_code == 200
        assert del_resp.json() == {"ok": True}

        list_resp = client.get("/api/categories", headers=auth_headers)
        assert len(list_resp.json()) == 0

    def test_delete_category_with_children(self, client, auth_headers):
        """Deleting parent category cascades to children."""
        parent_resp = client.post(
            "/api/categories",
            json={"name": "Parent"},
            headers=auth_headers,
        )
        parent_id = parent_resp.json()["id"]

        client.post(
            "/api/categories",
            json={"name": "Child", "parent_id": parent_id},
            headers=auth_headers,
        )

        del_resp = client.delete(
            f"/api/categories/{parent_id}", headers=auth_headers
        )
        assert del_resp.status_code == 200

        list_resp = client.get("/api/categories", headers=auth_headers)
        assert list_resp.json() == []

    def test_delete_nonexistent_category(self, client, auth_headers):
        """Deleting non-existent category returns 404."""
        resp = client.delete(
            "/api/categories/nonexistent", headers=auth_headers
        )
        assert resp.status_code == 404
