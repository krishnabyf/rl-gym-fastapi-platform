import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.services.jobs import benchmark_jobs, simulation_jobs


@pytest.fixture(autouse=True)
def reset_job_stores() -> None:
    simulation_jobs.reset()
    benchmark_jobs.reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())

