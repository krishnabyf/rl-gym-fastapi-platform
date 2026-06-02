from fastapi import APIRouter

from app.api.v1.routes import benchmarks, environments, health, simulations

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(environments.router, prefix="/environments", tags=["environments"])
api_router.include_router(simulations.router, prefix="/simulations", tags=["simulations"])
api_router.include_router(benchmarks.router, prefix="/benchmarks", tags=["benchmarks"])

