
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.pitchpulse.main import app

client = TestClient(app)



@pytest.fixture
def mock_api_football_response():
    """Return fake API-Football JSON response"""
    return {
        "response": [
            {
                "player": {
                    "id": 276,
                    "name": "Erling Haaland",
                    "age": 24
                },
                "statistics": [
                    {
                        "team": {"name": "Manchester City"},
                        "games": {
                            "appearences": 35,
                            "minutes": 3024,
                            "position": "Attacker"
                        },
                        "goals": {
                            "total": 36,
                            "assists": 8
                        }
                    }
                ]
            }
        ]
    }


@patch("src.pitchpulse.clients.api_football.APIFootballClient.get_player_stats")
def test_get_player_stats_success(mock_get_stats, mock_api_football_response):

    mock_get_stats.return_value = mock_api_football_response

    response = client.get("/players/276/stats?season=2024")

    assert response.status_code == 200

    data = response.json()
    assert data["player_id"] == 276
    assert data["player_name"] == "Erling Haaland"
    assert data["team"] == "Manchester City"
    assert data["goals"] == 36
    assert data["assists"] == 8

    expected_goals_per_90 = round((36 / 3024) * 90, 2)
    assert data["goals_per_90"] == expected_goals_per_90


@patch("src.pitchpulse.clients.api_football.APIFootballClient.get_player_stats")
def test_get_player_stats_not_found(mock_get_stats):

    mock_get_stats.return_value = {"response": []}

    response = client.get("/players/99999/stats")

    assert response.status_code == 404
    assert "Player not found" in response.json()["detail"]


@patch("src.pitchpulse.clients.api_football.APIFootballClient.get_player_stats")
def test_get_player_stats_zero_minutes(mock_get_stats):
    """Test player with 0 minutes played (avoid division by zero)"""

    mock_get_stats.return_value = {
        "response": [
            {
                "player": {"id": 123, "name": "Bench Warmer"},
                "statistics": [
                    {
                        "team": {"name": "Test FC"},
                        "games": {"appearences": 0, "minutes": 0},
                        "goals": {"total": 0, "assists": 0}
                    }
                ]
            }
        ]
    }

    response = client.get("/players/123/stats")

    assert response.status_code == 200
    data = response.json()
    assert data["goals_per_90"] == 0.0
