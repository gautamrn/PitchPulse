from fastapi import FastAPI

# TODO (Step 3): Import routers when created
# from src.pitchpulse.routers import matches, players, teams

app = FastAPI(
    title="PitchPulse",
    description="Soccer Analytics Microservice",
    version="0.1.0"
)

# TODO (Step 3): Include routers
# app.include_router(matches.router, prefix="/matches", tags=["matches"])
# app.include_router(players.router, prefix="/players", tags=["players"])
# app.include_router(teams.router, prefix="/teams", tags=["teams"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "PitchPulse",
        "status": "operational",
        "message": "Soccer analytics microservice is running"
    }


@app.get("/health")
async def health_check():
    """
    Dedicated health check for container orchestration.
    Kubernetes/Docker will ping this endpoint to verify service is alive.
    """
    return {"status": "healthy"}
