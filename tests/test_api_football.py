import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.pitchpulse.clients.api_football import APIFootballClient
from src.pitchpulse.config import Settings


@pytest.fixture
def mock_settings():
    """Fixture for Settings object"""
    return Settings(
        api_football_key="test_key",
        api_football_base_url="https://test.api.com"
    )


@pytest.mark.asyncio
async def test_api_client_get_player_stats(mock_settings):
    """Test successful API call"""
    # Create a mock httpx client that will be injected
    mock_client = AsyncMock()

    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": [{"player": {"id": 1100, "name": "Haaland"}}]}

    # Set up the async get method to return the response
    mock_client.get.return_value = mock_response

    # Patch httpx.AsyncClient in the api_football module
    with patch("src.pitchpulse.clients.api_football.httpx.AsyncClient") as mock_httpx:
        mock_httpx.return_value = mock_client

        async with APIFootballClient(mock_settings) as client:
            result = await client.get_player_stats(1100, 2024)

    assert result == {"response": [{"player": {"id": 1100, "name": "Haaland"}}]}
    mock_client.get.assert_called_once_with(
        "/players",
        params={"id": 1100, "season": 2024}
    )


@pytest.mark.asyncio
async def test_api_client_without_context_manager(mock_settings):
    """Test that using client without context manager raises error"""
    client = APIFootballClient(mock_settings)

    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get_player_stats(1100, 2024)
