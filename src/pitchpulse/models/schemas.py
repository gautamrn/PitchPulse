
from pydantic import BaseModel, Field
from typing import Optional


class PlayerStatsResponse(BaseModel):
    player_id: int = Field(..., description = "Player ID")
    player_name: str = Field(..., description = "Player Name")
    team: Optional[str] = Field(None, description = "Team Name")
    position: Optional[str] = Field(None, description = "Player position")
    games_played: int = Field(0, description = "Total games played")
    minutes_played: int = Field(0, description = "Total minutes played")
    goals: int = Field(0, description = "Total goals scored")
    assists: int = Field(0, description = "Total assists")
    goals_per_90: float = Field(0.0, description = "Goals per 90 minutes")

    class Config:
        json_schema_extra = {
            "example": {
            "player_id": 276,
            "player_name": "Erling Haaland",
            "team": "Manchester City",
            "position": "Attacker",
            "games_played": 35,
            "minutes_played": 3024,
            "goals": 36,
            "assists": 8,
            "goals_per_90": 1.07
            }
        }
