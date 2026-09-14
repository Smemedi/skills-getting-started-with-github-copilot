"""
Tests for the POST /activities/{activity_name}/unregister endpoint.
"""

import pytest


class TestUnregister:
    """Tests for unregistering from activities."""

    def test_unregister_successful(self, client):
        """Test successful unregister returns 200 and correct message."""
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email in response.json()["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister removes the student from participants list."""
        email = "michael@mergington.edu"
        
        # Get initial participants
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        
        # Unregister
        client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        
        # Verify participant was removed
        response = client.get("/activities")
        new_participants = response.json()["Chess Club"]["participants"]
        assert email not in new_participants
        assert len(new_participants) == initial_count - 1

    def test_unregister_nonexistent_activity(self, client):
        """Test unregister from non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_not_signed_up(self, client):
        """Test unregister for student not signed up returns 400."""
        email = "notstudent@mergington.edu"  # Not signed up for anything
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_already_unregistered(self, client):
        """Test unregister twice returns 400 on second attempt."""
        email = "michael@mergington.edu"
        
        # First unregister succeeds
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Second unregister fails
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_from_different_activity(self, client):
        """Test unregister from activity student wasn't in."""
        email = "michael@mergington.edu"  # In Chess Club
        
        # Try to unregister from Soccer (not signed up)
        response = client.post(
            "/activities/Soccer/unregister",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_integration_activities_updated(self, client):
        """Test that activities list reflects unregister immediately."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Unregister
        client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Verify removed from activities list
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

    def test_signup_then_unregister_integration(self, client):
        """Test full flow: signup then unregister."""
        email = "fullflow@mergington.edu"
        activity = "Debate Club"
        
        # Initial state: not signed up
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]
        
        # Signup
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify signed up
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]
        
        # Unregister
        response = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify unregistered
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]
