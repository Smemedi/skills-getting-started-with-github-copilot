"""
Pytest configuration and fixtures for testing the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def activities_data():
    """Provide a fresh copy of activities data for each test."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball": {
            "description": "Competitive basketball team and practices",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Soccer": {
            "description": "Outdoor soccer matches and drills",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore various art mediums including painting and sculpture",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu"]
        },
        "Music Band": {
            "description": "Join our school band and perform at events",
            "schedule": "Mondays, Wednesdays, Fridays, 3:45 PM - 4:45 PM",
            "max_participants": 25,
            "participants": ["liam@mergington.edu", "noah@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "mason@mergington.edu"]
        }
    }


@pytest.fixture
def client(activities_data):
    """Provide a TestClient with fresh activities data for each test."""
    # Replace the app's activities with fresh test data
    import src.app
    original_activities = src.app.activities.copy()
    src.app.activities.clear()
    src.app.activities.update(activities_data)
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore original activities after test
    src.app.activities.clear()
    src.app.activities.update(original_activities)
