from fastapi import APIRouter, HTTPException, status

from app.domain.registry import environment_registry
from app.domain.schemas import EnvironmentInfo

router = APIRouter()


@router.get("", response_model=list[EnvironmentInfo])
async def list_environments() -> list[EnvironmentInfo]:
    return environment_registry.list()


@router.get("/{environment_id}", response_model=EnvironmentInfo)
async def get_environment(environment_id: str) -> EnvironmentInfo:
    environment = environment_registry.get(environment_id)
    if environment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Environment '{environment_id}' is not registered.",
        )
    return environment.info

