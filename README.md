# PitchPulse

A containerized soccer analytics microservice deployed to AWS, providing player statistics through a REST API with Redis caching.

## Live API

**Base URL:** `http://54.242.60.48:8000`

- Interactive API Docs: http://54.242.60.48:8000/docs
- Health Check: http://54.242.60.48:8000/health
- Example: http://54.242.60.48:8000/players/276/stats?season=2023

## What It Does

Fetches player statistics from API-Football and calculates custom analytics like goals per 90 minutes. Uses Redis caching to reduce API costs by 80% and improve response times.

## Tech Stack

**Backend:** Python 3.11, FastAPI, Pydantic

**Infrastructure:** AWS ECS Fargate, ElastiCache Redis, ECR

**DevOps:** Docker, Docker Compose, GitHub Actions

**Testing:** pytest (89% coverage)

## Architecture

```
User Request
    ↓
AWS ECS Fargate (FastAPI Container)
    ↓
Redis Cache (5-min TTL)
    ↓ (cache miss)
API-Football External API
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Docker Compose
docker-compose up

# Run tests
pytest tests/ --cov=src/pitchpulse
```

## API Endpoints

### Get Player Stats
```
GET /players/{player_id}/stats?season={year}
```

**Example Response:**
```json
{
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
```

## Deployment

Deployed to AWS ECS Fargate with:
- Multi-stage Docker builds for optimized image size
- Redis caching via AWS ElastiCache
- Automated CI/CD through GitHub Actions
- CloudWatch logging for monitoring
- VPC networking with security groups

## Project Structure

```
PitchPulse/
├── src/pitchpulse/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Environment configuration
│   ├── models/
│   │   └── schemas.py       # Pydantic response models
│   ├── clients/
│   │   ├── api_football.py  # External API client
│   │   └── cache.py         # Redis cache client
│   └── routers/
│       └── players.py       # Player endpoints
├── tests/                   # Unit tests with mocking
├── Dockerfile               # Multi-stage container build
├── docker-compose.yml       # Local multi-container setup
└── requirements.txt         # Python dependencies
```

## Features

- Async request handling for concurrent API calls
- Cache-aside pattern with Redis (5-minute TTL)
- Pydantic schema validation
- Auto-generated OpenAPI documentation
- Comprehensive error handling
- 89% test coverage with pytest
- CI/CD pipeline with automated testing

## Author

Gautam - CS Student at University of Michigan
