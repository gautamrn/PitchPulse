
import httpx
from typing import Dict, Any
from src.pitchpulse.config import Settings


class APIFootballClient:
    def __init__(self, settings: Settings):
        self.base_url = settings.api_football_base_url
        self.api_key = settings.api_football_key
        self.headers = {"x-apisports-key": self.api_key}
        self._client = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url = self.base_url,
            headers = self.headers,
            timeout = 10.0
        )
        return self
    

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()


    async def get_player_stats(self, player_id: int, season: int = 2024) -> Dict[str, Any]:
        
        if not self._client:
            raise RuntimeError("Client not initialized")
        
        response = await self._client.get(
            "/players",
            params = {"id": player_id, "season": season}
        )

        response.raise_for_status()

        return response.json()

