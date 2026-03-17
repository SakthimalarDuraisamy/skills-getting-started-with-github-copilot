import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store initial state
    initial_activities = {
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
        "Tennis Team": {
            "description": "Competitive tennis training and matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Basketball League": {
            "description": "Join our basketball team for practices and games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["ryan@mergington.edu", "chris@mergington.edu"]
        },
        "Art Studio": {
            "description": "Learn painting, drawing, and other visual arts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Learn and perform music with the school band",
            "schedule": "Mondays and Fridays, 4:00 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop critical thinking and public speaking skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore physics, chemistry, and biology through hands-on experiments",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
        }
    }
    
    # Clear and reset
    activities.clear()
    for activity_name, activity_data in initial_activities.items():
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": activity_data["participants"].copy()
        }
    
    yield


def test_get_activities_returns_all_activities_and_participants():
    """Test that GET /activities returns all activities and participants"""
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_post_signup_adds_participant():
    """Test that POST /activities/{activity}/signup adds a participant"""
    # Arrange
    client = TestClient(app)
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={new_email}")
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert new_email in activities["Chess Club"]["participants"]


def test_post_signup_twice_same_email_returns_400():
    """Test that signing up twice with the same email returns 400"""
    # Arrange
    client = TestClient(app)
    email = "test@mergington.edu"
    
    # Act - First signup
    response1 = client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Act - Second signup with same email
    response2 = client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Student already signed up for this activity"


def test_delete_removes_participant():
    """Test that DELETE /activities/{activity}/participants removes a participant"""
    # Arrange
    client = TestClient(app)
    email = "michael@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/Chess Club/participants?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    assert email not in activities["Chess Club"]["participants"]


def test_delete_nonexistent_participant_returns_404():
    """Test that DELETE with nonexistent participant returns 404"""
    # Arrange
    client = TestClient(app)
    email = "nonexistent@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/Chess Club/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"
