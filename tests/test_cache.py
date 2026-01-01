import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.pitchpulse.clients.cache import RedisCache
from src.pitchpulse.config import Settings


@pytest.fixture
def mock_settings():
    """Fixture for Settings object"""
    return Settings(redis_url="redis://localhost:6379")


@pytest.mark.asyncio
@patch("src.pitchpulse.clients.cache.redis.from_url")
async def test_cache_get_hit(mock_redis_from_url, mock_settings):
    """Test cache GET when value exists"""
    mock_client = AsyncMock()
    mock_client.get.return_value = '{"key": "value"}'
    mock_redis_from_url.return_value = mock_client

    async with RedisCache(mock_settings) as cache:
        result = await cache.get("test_key")

    assert result == {"key": "value"}
    mock_client.get.assert_called_once_with("test_key")


@pytest.mark.asyncio
@patch("src.pitchpulse.clients.cache.redis.from_url")
async def test_cache_get_miss(mock_redis_from_url, mock_settings):
    """Test cache GET when value doesn't exist"""
    mock_client = AsyncMock()
    mock_client.get.return_value = None
    mock_redis_from_url.return_value = mock_client

    async with RedisCache(mock_settings) as cache:
        result = await cache.get("nonexistent_key")

    assert result is None


@pytest.mark.asyncio
@patch("src.pitchpulse.clients.cache.redis.from_url")
async def test_cache_set(mock_redis_from_url, mock_settings):
    """Test cache SET operation"""
    mock_client = AsyncMock()
    mock_redis_from_url.return_value = mock_client

    test_data = {"player_id": 276, "name": "Haaland"}

    async with RedisCache(mock_settings) as cache:
        await cache.set("test_key", test_data, ttl=300)

    mock_client.setex.assert_called_once()
    call_args = mock_client.setex.call_args[0]
    assert call_args[0] == "test_key"
    assert call_args[1] == 300


@pytest.mark.asyncio
async def test_cache_get_without_context_manager(mock_settings):
    """Test that using cache without context manager raises error"""
    cache = RedisCache(mock_settings)

    with pytest.raises(RuntimeError, match="Redis client not initialized"):
        await cache.get("test_key")
