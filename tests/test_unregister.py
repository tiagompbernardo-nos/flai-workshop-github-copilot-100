"""Tests for unregister functionality"""

import pytest


def test_unregister_success(client):
    """Test successfully unregistering from an activity"""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    # First signup
    email = "unregister_test@mergington.edu"
    activity = "Basketball Team"
    
    client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Then unregister
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity]["participants"]


def test_unregister_not_signed_up_fails(client):
    """Test that unregistering someone not signed up fails"""
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"].lower()


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregister from non-existent activity fails"""
    response = client.post(
        "/activities/Fake Activity/unregister",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
