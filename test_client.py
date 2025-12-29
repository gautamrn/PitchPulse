"""
Quick test script for API-Football client.
Run this to verify your async client works!

Usage:
    python test_client.py
"""

import asyncio
from src.pitchpulse.config import get_settings
from src.pitchpulse.clients.api_football import APIFootballClient


async def test_player_stats():
    """Test fetching player stats from API-Football"""
    settings = get_settings()

    print(f"API Key loaded: {settings.api_football_key[:10]}...")
    print(f"Base URL: {settings.api_football_base_url}\n")

    async with APIFootballClient(settings) as client:
        print("Fetching stats for player ID 1100 (Erling Haaland)...")
        data = await client.get_player_stats(player_id=1100, season=2024)

        print("\n✅ Success! Raw API response:")
        print(f"Response keys: {data.keys()}")

        if data.get("response"):
            player_info = data["response"][0]["player"]
            print(f"\nPlayer: {player_info['name']}")
            print(f"Age: {player_info['age']}")
            print(f"Nationality: {player_info['nationality']}")


if __name__ == "__main__":
    asyncio.run(test_player_stats())
