from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import settings
from app.domain.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        environment=settings.app_env,
        checked_at=datetime.now(UTC),
    )

