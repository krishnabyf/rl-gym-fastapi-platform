from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class JobStatus(StrEnum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"


class PolicyName(StrEnum):
    random = "random"
    greedy = "greedy"


class HealthResponse(BaseModel):
    status: Literal["ok"]
    app: str
    environment: str
    checked_at: datetime


class EnvironmentInfo(BaseModel):
    id: str
    name: str
    description: str
    observation_shape: list[int]
    action_space: list[str]
    max_reward: float


class SimulationRequest(BaseModel):
    environment_id: str = Field(default="gridworld-v0")
    episodes: int = Field(default=5, ge=1, le=500)
    max_steps: int = Field(default=50, ge=1, le=2_000)
    policy: PolicyName = PolicyName.greedy
    seed: int | None = Field(default=None, ge=0)


class EpisodeMetric(BaseModel):
    episode: int
    steps: int
    reward: float
    success: bool
    final_observation: dict[str, Any]


class SimulationResult(BaseModel):
    environment_id: str
    policy: PolicyName
    episodes: int
    average_reward: float
    success_rate: float
    metrics: list[EpisodeMetric]


class BenchmarkRequest(BaseModel):
    environment_id: str = Field(default="gridworld-v0")
    policies: list[PolicyName] = Field(
        default_factory=lambda: [PolicyName.random, PolicyName.greedy]
    )
    episodes: int = Field(default=10, ge=1, le=500)
    max_steps: int = Field(default=60, ge=1, le=2_000)
    seed: int | None = Field(default=None, ge=0)

    @field_validator("policies")
    @classmethod
    def policies_must_be_unique(cls, value: list[PolicyName]) -> list[PolicyName]:
        if not value:
            raise ValueError("At least one policy is required.")
        if len(set(value)) != len(value):
            raise ValueError("Policies must be unique.")
        return value


class BenchmarkPolicyResult(BaseModel):
    policy: PolicyName
    average_reward: float
    success_rate: float
    average_steps: float


class BenchmarkResult(BaseModel):
    environment_id: str
    episodes: int
    policies: list[BenchmarkPolicyResult]
    best_policy: PolicyName


class JobResponse(BaseModel):
    id: str
    status: JobStatus
    kind: str
