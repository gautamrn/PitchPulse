
from fastapi import APIRouter, Depends, HTTPException
from src.pitchpulse.config import Settings, get_settings
from src.pitchpulse.clients.api_football import APIFootballClient
from src.pitchpulse.models.schemas import PlayerStatsResponse

router = APIRouter()


@router.get("/{player_id}/stats", response_model=PlayerStatsResponse)
async def get_player_stats(
    player_id: int,
    season: int = 2024,
    settings: Settings = Depends(get_settings)
):
    

    try:
        async with APIFootballClient(settings) as client:
            raw_data = await client.get_player_stats(player_id, season)

        if not raw_data.get("response"):
            raise HTTPException(status_code = 404, detail = "Player not found")

        player_data = raw_data["response"][0]["player"]
        stats_data = raw_data["response"][0]["statistics"][0]

        minutes_played = stats_data.get("games", {}).get("minutes", 0)
        goals = stats_data.get("goals", {}).get("total", 0)
        assists = stats_data.get("goals", {}).get("assists", 0)
        games_played = stats_data.get("games", {}).get("appearances", 0)


        if minutes_played > 0:
            goals_per_90 = (goals/minutes_played) * 90
        else: 
            goals_per_90 = 0

        return PlayerStatsResponse(
            player_id = player_id,
            player_name = player_data["name"],
            team = stats_data.get("team", {}).get("name", "Unknown"),
            position = stats_data.get("games", {}).get("position"),
            games_played = games_played,
            minutes_played = minutes_played,
            goals = goals,
            assists = assists,
            goals_per_90 = round(goals_per_90, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch player stats: {str(e)}"
        )


# ==============================================================================
# EXPLANATION SECTION (Read after implementing)
# ==============================================================================
#
# What is APIRouter()?
# - Creates a modular router (can be included in main app)
# - Keeps code organized (players.py, matches.py, teams.py)
# - Allows versioning (v1/players, v2/players)
#
# What is @router.get("/{player_id}/stats")?
# - Decorator that creates GET endpoint
# - {player_id} is path parameter (captured from URL)
# - Combined with router prefix to become /players/276/stats
#
# What is response_model=PlayerStatsResponse?
# - Tells FastAPI to validate response against this Pydantic model
# - Auto-generates OpenAPI docs
# - Converts Python object to JSON automatically
#
# What is Depends(get_settings)?
# - Dependency injection pattern
# - FastAPI calls get_settings() and passes result to function
# - Cached by @lru_cache, so very efficient
#
# What is HTTPException?
# - FastAPI's way of returning error responses
# - status_code=404 → HTTP 404 Not Found
# - status_code=500 → HTTP 500 Internal Server Error
# - Client receives JSON: {"detail": "Player not found"}
#
# Why use .get() with defaults?
# - API-Football might not return all fields
# - .get("minutes", 0) returns 0 if "minutes" key missing
# - Prevents KeyError exceptions
#
# Why "or 0" after .get()?
# - API-Football sometimes returns None
# - "None or 0" evaluates to 0
# - Ensures we always have a number, not None
#
# ==============================================================================
