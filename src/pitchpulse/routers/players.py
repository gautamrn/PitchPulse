
from fastapi import APIRouter, Depends, HTTPException
from src.pitchpulse.config import Settings, get_settings
from src.pitchpulse.clients.api_football import APIFootballClient
from src.pitchpulse.clients.cache import RedisCache
from src.pitchpulse.models.schemas import PlayerStatsResponse

router = APIRouter()


@router.get("/{player_id}/stats", response_model=PlayerStatsResponse)
async def get_player_stats(
    player_id: int,
    season: int = 2024,
    settings: Settings = Depends(get_settings)
):
   
    cache_key = f"player:{player_id}:season:{season}"

    try:
        async with RedisCache(settings) as cache:
            cached_data = await cache.get(cache_key)
            
            if cached_data:
                return PlayerStatsResponse(**cached_data)



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

        response_data = {
            "player_id": player_id,
            "player_name": player_data["name"],
            "team": stats_data.get("team", {}).get("name", "Unknown"),
            "position": stats_data.get("games", {}).get("position"),
            "games_played": games_played,
            "minutes_played": minutes_played,
            "goals": goals,
            "assists": assists,
            "goals_per_90": round(goals_per_90, 2)
        }


        async with RedisCache(settings) as cache:
            await cache.set(cache_key, response_data, settings.cache_ttl)

        return PlayerStatsResponse(**response_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch player stats: {str(e)}"
        )
