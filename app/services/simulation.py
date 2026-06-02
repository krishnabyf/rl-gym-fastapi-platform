from random import Random

from app.domain.registry import environment_registry
from app.domain.schemas import EpisodeMetric, SimulationRequest, SimulationResult
from app.services.jobs import simulation_jobs
from app.services.policies import policy_engine


class SimulationService:
    async def run_simulation_job(self, job_id: str, request: SimulationRequest) -> None:
        simulation_jobs.mark_running(job_id)
        try:
            result = self.run(request)
        except Exception as exc:  # pragma: no cover - defensive job boundary
            simulation_jobs.mark_failed(job_id, str(exc))
            return
        simulation_jobs.mark_succeeded(job_id, result.model_dump(mode="json"))

    def run(self, request: SimulationRequest) -> SimulationResult:
        environment = environment_registry.get(request.environment_id)
        if environment is None:
            msg = f"Environment '{request.environment_id}' is not registered."
            raise ValueError(msg)

        metrics: list[EpisodeMetric] = []
        random = Random(request.seed)

        for episode in range(1, request.episodes + 1):
            episode_seed = None if request.seed is None else request.seed + episode
            observation = environment.reset(seed=episode_seed)
            total_reward = 0.0
            success = False
            steps_taken = 0

            for step in range(1, request.max_steps + 1):
                action = policy_engine.choose_action(
                    request.policy,
                    observation,
                    environment.info.action_space,
                    random,
                )
                step_result = environment.step(action)
                observation = step_result.observation
                total_reward += step_result.reward
                steps_taken = step

                if step_result.terminated:
                    success = True
                    break

            metrics.append(
                EpisodeMetric(
                    episode=episode,
                    steps=steps_taken,
                    reward=round(total_reward, 4),
                    success=success,
                    final_observation=observation,
                )
            )

        average_reward = sum(metric.reward for metric in metrics) / len(metrics)
        success_rate = sum(1 for metric in metrics if metric.success) / len(metrics)

        return SimulationResult(
            environment_id=request.environment_id,
            policy=request.policy,
            episodes=request.episodes,
            average_reward=round(average_reward, 4),
            success_rate=round(success_rate, 4),
            metrics=metrics,
        )


simulation_service = SimulationService()

