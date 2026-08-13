"""Tests for GET / root endpoint"""

import pytest


class TestRootEndpoint:
    """Test suite for the GET / root endpoint"""

    def test_root_redirect_to_index(self, client):
        """
        Test that GET / redirects to /static/index.html.
        
        Arrange: Prepare test client
        Act: Send GET request to /
        Assert: Verify redirect response and location
        """
        # Arrange
        expected_redirect_url = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url

    def test_root_redirect_follows(self, client):
        """
        Test that following the redirect from / reaches index.html.
        
        Arrange: Prepare test client
        Act: Send GET request to / with follow_redirects=True
        Assert: Verify final response is HTML
        """
        # Arrange (none needed)

        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_root_returns_temporary_redirect(self, client):
        """
        Test that GET / returns 307 Temporary Redirect status.
        
        Arrange: Prepare test client
        Act: Send GET request to /
        Assert: Verify status code is 307 (temporary redirect, not 301 or 302)
        """
        # Arrange (none needed)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
