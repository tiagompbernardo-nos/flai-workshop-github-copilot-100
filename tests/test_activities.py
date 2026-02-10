"""Tests for the activities endpoint"""

import pytest


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 9  # Should have 9 activities


def test_get_activities_contains_required_fields(client):
    """Test that activities have required fields"""
    response = client.get("/activities")
    data = response.json()
    
    # Check a specific activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_participants_not_empty(client):
    """Test that some activities have participants"""
    response = client.get("/activities")
    data = response.json()
    
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) > 0
    assert "michael@mergington.edu" in chess_club["participants"]
