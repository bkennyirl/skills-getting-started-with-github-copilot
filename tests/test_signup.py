"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


class TestSignupEndpoint:
    """Test suite for the POST signup endpoint"""

    def test_signup_success(self, client):
        """
        Test successful signup of a new participant.
        
        Arrange: Define activity name and new participant email
        Act: Send POST signup request
        Assert: Verify response is successful and participant was added
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        activities = client.get("/activities").json()

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert "Signed up" in response.json()["message"]

    def test_signup_activity_not_found(self, client):
        """
        Test signup for a non-existent activity returns 404.
        
        Arrange: Define a non-existent activity name and email
        Act: Send POST signup request
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_student(self, client):
        """
        Test that a student cannot sign up twice for the same activity.
        
        Arrange: Define an activity and a student already in that activity
        Act: Try to sign up the same student again
        Assert: Verify 400 error is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_activity_full(self, client):
        """
        Test that signup fails when activity is at capacity.
        
        Arrange: Use Tennis Club which has max_participants=18 with only 1 current
        Act: Fill up the activity and try one more signup
        Assert: Verify 400 error for full activity
        """
        # Arrange
        activity_name = "Tennis Club"
        base_email = "tennis_student{}"
        
        # Get current state
        activities = client.get("/activities").json()
        current_participants = len(activities[activity_name]["participants"])
        max_participants = activities[activity_name]["max_participants"]
        spots_available = max_participants - current_participants  # Should be 17

        # Sign up students until the activity is full
        for i in range(spots_available):
            email = base_email.format(i)
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200

        # Now try to sign up one more student (should fail)
        overflow_email = "overflow@mergington.edu"
        response = client.post(f"/activities/{activity_name}/signup?email={overflow_email}")

        # Assert
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()

    def test_signup_participant_added_to_correct_activity(self, client):
        """
        Test that a participant is added to the correct activity only.
        
        Arrange: Get initial state and define test data
        Act: Sign up for an activity
        Assert: Verify participant added only to target activity
        """
        # Arrange
        target_activity = "Programming Class"
        other_activity = "Gym Class"
        email = "verify@mergington.edu"
        
        initial_target = client.get(f"/activities").json()[target_activity]["participants"].copy()
        initial_other = client.get(f"/activities").json()[other_activity]["participants"].copy()

        # Act
        response = client.post(f"/activities/{target_activity}/signup?email={email}")

        # Assert
        updated_activities = client.get("/activities").json()
        assert email in updated_activities[target_activity]["participants"]
        assert email not in updated_activities[other_activity]["participants"]
        assert len(updated_activities[other_activity]["participants"]) == len(initial_other)

    @pytest.mark.parametrize("email", [
        "simple@mergington.edu",
        "with.dot@mergington.edu",
        "with_underscore@mergington.edu",
        "UPPERCASE@MERGINGTON.EDU",
    ])
    def test_signup_with_various_email_formats(self, client, email):
        """
        Test signup with various valid email formats.
        
        Arrange: Define various valid email formats
        Act: Sign up with each email format
        Assert: All signups succeed
        """
        # Arrange
        activity_name = "Programming Class"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_signup_response_contains_message(self, client):
        """
        Test that signup response contains proper message format.
        
        Arrange: Define test data
        Act: Send signup request
        Assert: Verify response message format
        """
        # Arrange
        activity_name = "Chess Club"
        email = "message@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
