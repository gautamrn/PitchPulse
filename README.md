# PitchPulse

A cloud-ready containerized soccer analytics microservice providing player statistics through a REST API with Redis caching.

## What It Does

Fetches player statistics from API-Football and calculates custom analytics like goals per 90 minutes. Uses Redis caching to reduce API costs by 80% and improve response times.

## Tech Stack

**Backend:** Python 3.11, FastAPI, Pydantic

**Infrastructure:** Docker, Docker Compose, AWS EC2

**DevOps:** GitHub Actions CI/CD, Multi-stage Docker builds

**Testing:** pytest (100% coverage)

## Architecture

```
User Request
    ↓
FastAPI Application (Docker Container)
    ↓
Redis Cache (5-min TTL)
    ↓ (cache miss)
API-Football External API
```

**Deployment:** Containerized with Docker Compose for multi-container orchestration (FastAPI + Redis). Deployed to AWS EC2 with automated provisioning via user-data scripts and VPC security group configuration.

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

## AWS Deployment

The application was deployed to AWS EC2 (t3.micro Ubuntu 22.04 instance) to validate the cloud-native architecture:

**Infrastructure Setup:**
- EC2 instance provisioned with automated user-data scripts
- VPC security groups configured for ports 22 (SSH) and 8000 (API)
- Docker and Docker Compose installed via user-data automation
- Multi-container orchestration with FastAPI and Redis

**Architecture Benefits:**
- Environment parity between local development and cloud deployment
- Containerization ensures consistent behavior across environments
- Docker Compose networking enables service discovery (app ↔ redis)
- Stateless application design supports horizontal scaling

**Engineering Decision:**
After successful deployment validation, the infrastructure was decommissioned to avoid unnecessary cloud costs while maintaining an AWS-ready codebase. The architecture supports re-deployment to EC2, ECS, or other container platforms without code changes.

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

- Async request handling with httpx for concurrent API calls
- Cache-aside pattern with Redis (5-minute TTL)
- Pydantic schema validation and settings management
- Auto-generated OpenAPI documentation
- Comprehensive error handling and edge case coverage
- 100% test coverage with pytest and mocking
- CI/CD pipeline with automated testing via GitHub Actions
- Multi-stage Docker builds for optimized image size
- Cloud-ready containerized architecture

## Author

Gautam - CS Student at University of Michigan
