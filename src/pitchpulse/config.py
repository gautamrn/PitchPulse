import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_football_key: str = ""
    api_football_base_url: str = "https://v3.football.api-sports.io"

    redis_url: str = "redis://localhost:6379"
    cache_ttl: int = 300


    environment: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()