"""Tests for GET /activities endpoint"""

import pytest


class TestActivitiesEndpoint:
    """Test suite for the GET /activities endpoint"""

    def test_get_activities_success(self, client):
        """
        Verify that GET /activities returns all activities with correct structure.
        
        Arrange: Prepare test client
        Act: Send GET request to /activities
        Assert: Verify response contains activities with correct data structure
        """
        # Arrange
        expected_keys = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Verify each activity has the correct structure
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert activity_data.keys() == expected_keys

    def test_activities_have_correct_data_types(self, client):
        """
        Verify that activity fields have correct data types.
        
        Arrange: Prepare test client
        Act: Send GET request to /activities
        Assert: Verify data types of activity fields
        """
        # Arrange (none needed)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
            
            # Each participant should be an email string
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant

    def test_activities_participant_count_is_valid(self, client):
        """
        Verify that participant count does not exceed max_participants.
        
        Arrange: Prepare test client
        Act: Send GET request to /activities
        Assert: Verify participant count is valid
        """
        # Arrange (none needed)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            participant_count = len(activity_data["participants"])
            max_participants = activity_data["max_participants"]
            assert participant_count <= max_participants, \
                f"{activity_name}: participants ({participant_count}) exceed max ({max_participants})"

    def test_activities_are_not_empty(self, client):
        """
        Verify that at least one activity is available.
        
        Arrange: Prepare test client
        Act: Send GET request to /activities
        Assert: Verify activities list is not empty
        """
        # Arrange (none needed)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert len(data) > 0, "No activities available"
        
        # Verify expected activities exist
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        for activity in expected_activities:
            assert activity in data, f"Expected activity '{activity}' not found"
