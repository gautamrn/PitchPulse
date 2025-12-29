import pytest
from fastapi.testclient import TestClient
from src.pitchpulse.main import app

# TestClient makes synchronous requests (easier for testing)
client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct service info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "PitchPulse"
    assert data["status"] == "operational"


def test_health_check():
    """Test health check endpoint for container orchestration"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# TODO (Step 3): Add tests for API-Football endpoints
# @pytest.mark.asyncio
# async def test_get_match_stats():
#     """Test fetching match statistics"""
#     pass


# TODO (Step 4): Add integration tests with mocked API responses
# def test_api_football_error_handling():
#     """Test graceful handling of API-Football failures"""
#     pass
