from fastapi import FastAPI
from src.pitchpulse.routers import players

app = FastAPI(
    title="PitchPulse",
    description="Soccer Analytics Microservice",
    version="0.1.0"
)

# Register players router
# This creates all /players/* endpoints
app.include_router(players.router, prefix="/players", tags=["players"])


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
