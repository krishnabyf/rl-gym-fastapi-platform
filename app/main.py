from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="FastAPI backend for RL simulation and benchmarking workflows.",
    )
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()

