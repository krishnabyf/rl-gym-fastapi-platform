from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.domain.schemas import JobResponse, SimulationRequest, SimulationResult
from app.services.jobs import simulation_jobs
from app.services.simulation import simulation_service

router = APIRouter()


@router.post("", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_simulation(
    payload: SimulationRequest,
    background_tasks: BackgroundTasks,
) -> JobResponse:
    job = simulation_jobs.create("simulation", payload)
    background_tasks.add_task(simulation_service.run_simulation_job, job.id, payload)
    return JobResponse(id=job.id, status=job.status, kind=job.kind)


@router.get("/{job_id}", response_model=SimulationResult)
async def get_simulation(job_id: str) -> SimulationResult:
    job = simulation_jobs.get(job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Simulation job not found.",
        )
    if job.error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=job.error)
    if job.result is None:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Simulation is still running.",
        )
    return SimulationResult.model_validate(job.result)
