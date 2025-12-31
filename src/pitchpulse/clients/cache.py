import redis.asyncio as redis
from typing import Optional, Any
import json
from src.pitchpulse.config import Settings


class RedisCache:

    def __init__(self, settings: Settings):
        self.redis_url = settings.redis_url
        self._client: Optional[redis.Redis] = None


    async def __aenter__(self):
        self._client = redis.from_url(
            self.redis_url,
            decode_responses=True
        )
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.close()
        


    async def get(self, key: str) -> Optional[dict]:
        if not self._client:
            raise RuntimeError("Redis client not initialized. Use 'async with' pattern.")

        value = await self._client.get(key)

        if value:
            return json.loads(value)

        return None
        

    async def set(self, key: str, value: dict, ttl: int = 300) -> None:
        json_value = json.dumps(value)
        await self._client.setex(key, ttl, json_value)
