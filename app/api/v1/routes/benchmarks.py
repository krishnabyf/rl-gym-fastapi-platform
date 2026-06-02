from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.domain.schemas import BenchmarkRequest, BenchmarkResult, JobResponse
from app.services.benchmark import benchmark_service
from app.services.jobs import benchmark_jobs

router = APIRouter()


@router.post("", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_benchmark(
    payload: BenchmarkRequest,
    background_tasks: BackgroundTasks,
) -> JobResponse:
    job = benchmark_jobs.create("benchmark", payload)
    background_tasks.add_task(benchmark_service.run_benchmark_job, job.id, payload)
    return JobResponse(id=job.id, status=job.status, kind=job.kind)


@router.get("/{job_id}", response_model=BenchmarkResult)
async def get_benchmark(job_id: str) -> BenchmarkResult:
    job = benchmark_jobs.get(job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benchmark job not found.",
        )
    if job.error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=job.error)
    if job.result is None:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Benchmark is still running.",
        )
    return BenchmarkResult.model_validate(job.result)
