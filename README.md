# RL Gym FastAPI Platform

Production-style backend for reinforcement-learning experimentation workflows. It exposes FastAPI endpoints for environment discovery, simulation jobs, policy evaluation, benchmarking, and service health.

This project is built to match Python/FastAPI backend work for RL/Gym platforms: async API design, typed request/response contracts, dependency-injected services, deterministic tests, Docker packaging, CI, and clean API docs.

## Why This Project Stands Out

- FastAPI app with versioned REST endpoints and typed Pydantic schemas.
- Async job lifecycle for simulations and benchmark runs.
- RL-style GridWorld environment with deterministic seeding and policy evaluation.
- Pluggable environment registry so Gymnasium/OpenAI Gym environments can be added later.
- In-memory repository for easy demo use, with a clear path to SQL persistence.
- Pytest coverage for health checks, environment listing, simulations, and benchmarks.
- Dockerfile, Compose file, Makefile, CI workflow, and production notes.

## Architecture

```text
app/
  api/v1/          HTTP route modules
  core/            settings, exceptions, logging
  domain/          Pydantic contracts and RL environment abstractions
  services/        orchestration for jobs, simulations, benchmarks
  workers/         background task helpers
tests/             API and service tests
docs/              production and extension notes
```

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health

## Example Requests

List environments:

```bash
curl http://127.0.0.1:8000/api/v1/environments
```

Run a simulation:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/simulations \
  -H "Content-Type: application/json" \
  -d '{"environment_id":"gridworld-v0","episodes":5,"max_steps":50,"policy":"greedy","seed":42}'
```

Run a benchmark:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/benchmarks \
  -H "Content-Type: application/json" \
  -d '{"environment_id":"gridworld-v0","policies":["random","greedy"],"episodes":10,"max_steps":60,"seed":7}'
```

## Testing

```bash
pytest
ruff check .
```

## Docker

```bash
docker compose up --build
```

## API Surface

- `GET /api/v1/health`
- `GET /api/v1/environments`
- `GET /api/v1/environments/{environment_id}`
- `POST /api/v1/simulations`
- `GET /api/v1/simulations/{job_id}`
- `POST /api/v1/benchmarks`
- `GET /api/v1/benchmarks/{job_id}`

## Production Notes

See [docs/production.md](docs/production.md) for deployment, observability, persistence, and security guidance.

## How To Extend With Gymnasium

See [docs/gymnasium-extension.md](docs/gymnasium-extension.md). The current implementation keeps the default environment lightweight and deterministic so the project can run anywhere, while the registry interface is ready for Gymnasium adapters.

