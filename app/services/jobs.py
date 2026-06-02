from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import Lock
from typing import Any
from uuid import uuid4

from app.core.config import settings
from app.domain.schemas import JobStatus


@dataclass
class JobRecord:
    id: str
    kind: str
    status: JobStatus
    payload: Any
    result: dict[str, Any] | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}
        self._lock = Lock()

    def create(self, kind: str, payload: Any) -> JobRecord:
        with self._lock:
            self._trim()
            job = JobRecord(id=str(uuid4()), kind=kind, status=JobStatus.queued, payload=payload)
            self._jobs[job.id] = job
            return job

    def get(self, job_id: str) -> JobRecord | None:
        with self._lock:
            return self._jobs.get(job_id)

    def mark_running(self, job_id: str) -> None:
        self._update(job_id, status=JobStatus.running)

    def mark_succeeded(self, job_id: str, result: dict[str, Any]) -> None:
        self._update(job_id, status=JobStatus.succeeded, result=result)

    def mark_failed(self, job_id: str, error: str) -> None:
        self._update(job_id, status=JobStatus.failed, error=error)

    def reset(self) -> None:
        with self._lock:
            self._jobs.clear()

    def _update(self, job_id: str, **changes: Any) -> None:
        with self._lock:
            job = self._jobs[job_id]
            for key, value in changes.items():
                setattr(job, key, value)
            job.updated_at = datetime.now(UTC)

    def _trim(self) -> None:
        overflow = len(self._jobs) - settings.job_retention_limit
        if overflow <= 0:
            return
        sorted_jobs = sorted(self._jobs.values(), key=lambda job: job.created_at)
        for job in sorted_jobs[:overflow]:
            self._jobs.pop(job.id, None)


simulation_jobs = JobStore()
benchmark_jobs = JobStore()

