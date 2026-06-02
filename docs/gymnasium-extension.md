# Gymnasium Extension Guide

The built-in GridWorld environment follows the same reset/step shape used by Gymnasium. To connect real Gymnasium environments:

1. Install the optional dependency:

   ```bash
   pip install -e ".[rl]"
   ```

2. Create an adapter that implements `RLEnvironment`.
3. Map Gymnasium observations into JSON-serializable dictionaries.
4. Register the adapter with `environment_registry.register("cartpole-v1", CartPoleFactory)`.

Example adapter shape:

```python
class GymnasiumAdapter(RLEnvironment):
    def __init__(self, env_id: str) -> None:
        import gymnasium as gym

        self.env = gym.make(env_id)

    def reset(self, seed: int | None = None) -> Observation:
        observation, _ = self.env.reset(seed=seed)
        return {"observation": observation.tolist()}

    def step(self, action: Action) -> StepResult:
        observation, reward, terminated, truncated, info = self.env.step(action)
        return StepResult(
            observation={"observation": observation.tolist()},
            reward=float(reward),
            terminated=terminated,
            truncated=truncated,
            info=info,
        )
```

Keep adapters thin. Put training loops, evaluation logic, and benchmark orchestration in services so routes stay small and testable.

