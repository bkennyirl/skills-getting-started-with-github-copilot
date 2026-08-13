"""Tests for DELETE /activities/{activity_name}/unregister endpoint"""

import pytest


class TestUnregisterEndpoint:
    """Test suite for the DELETE unregister endpoint"""

    def test_unregister_success(self, client):
        """
        Test successful removal of a participant from an activity.
        
        Arrange: Define activity and existing participant
        Act: Send DELETE unregister request
        Assert: Verify participant was removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        activities = client.get("/activities").json()

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert "Removed" in response.json()["message"]

    def test_unregister_activity_not_found(self, client):
        """
        Test unregister from non-existent activity returns 404.
        
        Arrange: Define a non-existent activity name
        Act: Send DELETE unregister request
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_participant_not_in_activity(self, client):
        """
        Test unregister of participant not in activity returns 404.
        
        Arrange: Define activity and participant not in that activity
        Act: Send DELETE unregister request
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notmember@mergington.edu"  # Not in Chess Club

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_removed_from_correct_activity(self, client):
        """
        Test that participant is removed from correct activity only.
        
        Arrange: Get initial state, define test activities and email
        Act: Unregister from one activity
        Assert: Verify removed from target, still in others
        """
        # Arrange
        # First, sign up the same person to multiple activities
        email = "testuser@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        client.post(f"/activities/{activity1}/signup?email={email}")
        client.post(f"/activities/{activity2}/signup?email={email}")

        # Act
        response = client.delete(f"/activities/{activity1}/unregister?email={email}")

        # Assert
        activities = client.get("/activities").json()
        assert email not in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_unregister_response_contains_message(self, client):
        """
        Test that unregister response contains proper message format.
        
        Arrange: Define test data with existing participant
        Act: Send DELETE unregister request
        Assert: Verify response message format
        """
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_then_signup_again(self, client):
        """
        Test that a participant can re-signup after being unregistered.
        
        Arrange: Define test data
        Act: Unregister, then sign up again
        Assert: Verify successful re-signup
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already in Programming Class

        # Act - Unregister
        response_delete = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        activities_after_delete = client.get("/activities").json()
        
        # Act - Sign up again
        response_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
        activities_after_signup = client.get("/activities").json()

        # Assert
        assert response_delete.status_code == 200
        assert email not in activities_after_delete[activity_name]["participants"]
        
        assert response_signup.status_code == 200
        assert email in activities_after_signup[activity_name]["participants"]

    def test_unregister_decreases_participant_count(self, client):
        """
        Test that unregister decreases the participant count.
        
        Arrange: Get initial participant count
        Act: Unregister a participant
        Assert: Verify count decreased by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        updated_activities = client.get("/activities").json()
        updated_count = len(updated_activities[activity_name]["participants"])

        # Assert
        assert response.status_code == 200
        assert updated_count == initial_count - 1
        assert initial_count > 0
