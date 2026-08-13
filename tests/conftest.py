"""Pytest configuration and shared fixtures for API tests"""

import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


# Store original activities state
ORIGINAL_ACTIVITIES = {
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
    "Basketball Team": {
        "description": "Competitive basketball team and practice sessions",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis instruction and match play",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["jessica@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and various art techniques",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater performance and acting skills",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore scientific experiments and discovery",
        "schedule": "Thursdays, 3:30 PM - 4:45 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays, 4:00 PM - 5:15 PM",
        "max_participants": 14,
        "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Provide a TestClient for making requests to the FastAPI app.
    
    Arrange: Reset activities to original state before each test for test isolation.
    """
    # Reset activities to original state (deep copy to avoid mutations)
    app_module.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)
    return TestClient(app_module.app)


@pytest.fixture
def sample_activities():
    """
    Provide sample activity data matching the app's data structure.
    
    Arrange: Create test data with known activities for use in test cases.
    """
    return copy.deepcopy(ORIGINAL_ACTIVITIES)
