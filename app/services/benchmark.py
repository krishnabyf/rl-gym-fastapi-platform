from app.domain.schemas import (
    BenchmarkPolicyResult,
    BenchmarkRequest,
    BenchmarkResult,
    SimulationRequest,
)
from app.services.jobs import benchmark_jobs
from app.services.simulation import simulation_service


class BenchmarkService:
    async def run_benchmark_job(self, job_id: str, request: BenchmarkRequest) -> None:
        benchmark_jobs.mark_running(job_id)
        try:
            result = self.run(request)
        except Exception as exc:  # pragma: no cover - defensive job boundary
            benchmark_jobs.mark_failed(job_id, str(exc))
            return
        benchmark_jobs.mark_succeeded(job_id, result.model_dump(mode="json"))

    def run(self, request: BenchmarkRequest) -> BenchmarkResult:
        policy_results: list[BenchmarkPolicyResult] = []

        for offset, policy in enumerate(request.policies):
            simulation = simulation_service.run(
                SimulationRequest(
                    environment_id=request.environment_id,
                    episodes=request.episodes,
                    max_steps=request.max_steps,
                    policy=policy,
                    seed=None if request.seed is None else request.seed + offset,
                )
            )
            average_steps = sum(metric.steps for metric in simulation.metrics) / len(
                simulation.metrics
            )
            policy_results.append(
                BenchmarkPolicyResult(
                    policy=policy,
                    average_reward=simulation.average_reward,
                    success_rate=simulation.success_rate,
                    average_steps=round(average_steps, 4),
                )
            )

        best_policy = max(
            policy_results,
            key=lambda result: (result.success_rate, result.average_reward),
        )
        return BenchmarkResult(
            environment_id=request.environment_id,
            episodes=request.episodes,
            policies=policy_results,
            best_policy=best_policy.policy,
        )


benchmark_service = BenchmarkService()
