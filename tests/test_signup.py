"""Tests for signup functionality"""

import pytest


def test_signup_for_activity_success(client):
    """Test successfully signing up for an activity"""
    email = "test@mergington.edu"
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds the participant"""
    email = "newstudent@mergington.edu"
    activity = "Programming Class"
    
    # Signup
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_fails(client):
    """Test that duplicate signup fails"""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_fails(client):
    """Test that signup for non-existent activity fails"""
    response = client.post(
        "/activities/Fake Activity/signup",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
