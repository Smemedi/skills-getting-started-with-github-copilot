"""
Tests for the GET /activities endpoint.
"""

import pytest


class TestActivities:
    """Tests for retrieving activities."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns 200 status code."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_all_activities(self, client, activities_data):
        """Test that all expected activities are returned."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name in activities_data.keys():
            assert activity_name in activities

    def test_get_activities_contains_required_fields(self, client):
        """Test that each activity contains required fields."""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for activity_name, activity in activities.items():
            for field in required_fields:
                assert field in activity, f"Activity '{activity_name}' missing field '{field}'"

    def test_get_activities_participants_is_list(self, client):
        """Test that participants field is a list."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity in activities.items():
            assert isinstance(activity["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"

    def test_get_activities_has_correct_participant_count(self, client, activities_data):
        """Test that activities have correct initial participant count."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, expected_data in activities_data.items():
            actual_participants = activities[activity_name]["participants"]
            expected_participants = expected_data["participants"]
            assert actual_participants == expected_participants, \
                f"Activity '{activity_name}' has incorrect participants"
