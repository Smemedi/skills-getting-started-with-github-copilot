"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestSignup:
    """Tests for signing up for activities."""

    def test_signup_successful(self, client):
        """Test successful signup returns 200 and correct message."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "newstudent@mergington.edu" in response.json()["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup adds the student to the participants list."""
        email = "newstudent@mergington.edu"
        
        # Get initial participants
        response = client.get("/activities")
        initial_participants = response.json()["Chess Club"]["participants"].copy()
        
        # Signup
        client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        
        # Verify participant was added
        response = client.get("/activities")
        new_participants = response.json()["Chess Club"]["participants"]
        assert email in new_participants
        assert len(new_participants) == len(initial_participants) + 1

    def test_signup_nonexistent_activity(self, client):
        """Test signup to non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email(self, client):
        """Test that duplicate signup returns 400."""
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_different_activity_same_email(self, client):
        """Test that same student can signup for different activities."""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Signup for different activity
        response = client.post(
            "/activities/Soccer/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify in both activities
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Soccer"]["participants"]

    def test_signup_activity_name_with_spaces(self, client):
        """Test signup for activity name with spaces works correctly."""
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": "newdev@mergington.edu"}
        )
        assert response.status_code == 200

    def test_signup_integration_activities_updated(self, client):
        """Test that activities list reflects signup immediately."""
        email = "integration@mergington.edu"
        activity = "Art Studio"
        
        # Signup
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Verify in activities list
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]
