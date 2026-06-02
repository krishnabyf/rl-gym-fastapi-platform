from collections.abc import Callable
from dataclasses import dataclass
from random import Random
from typing import Any

from app.domain.schemas import EnvironmentInfo

Action = str
Observation = dict[str, Any]


@dataclass(frozen=True)
class StepResult:
    observation: Observation
    reward: float
    terminated: bool
    truncated: bool
    info: dict[str, Any]


class RLEnvironment:
    info: EnvironmentInfo

    def reset(self, seed: int | None = None) -> Observation:
        raise NotImplementedError

    def step(self, action: Action) -> StepResult:
        raise NotImplementedError


class GridWorldEnvironment(RLEnvironment):
    info = EnvironmentInfo(
        id="gridworld-v0",
        name="GridWorld Navigation",
        description="Agent starts at top-left and learns to reach the goal at bottom-right.",
        observation_shape=[2],
        action_space=["up", "down", "left", "right"],
        max_reward=10.0,
    )

    def __init__(self, size: int = 5) -> None:
        self.size = size
        self.goal = (size - 1, size - 1)
        self.position = (0, 0)
        self.random = Random()

    def reset(self, seed: int | None = None) -> Observation:
        if seed is not None:
            self.random.seed(seed)
        self.position = (0, 0)
        return self._observation()

    def step(self, action: Action) -> StepResult:
        row, col = self.position
        if action == "up":
            row -= 1
        elif action == "down":
            row += 1
        elif action == "left":
            col -= 1
        elif action == "right":
            col += 1

        row = min(max(row, 0), self.size - 1)
        col = min(max(col, 0), self.size - 1)
        self.position = (row, col)

        terminated = self.position == self.goal
        reward = 10.0 if terminated else -0.1
        return StepResult(
            observation=self._observation(),
            reward=reward,
            terminated=terminated,
            truncated=False,
            info={"distance_to_goal": self._manhattan_distance()},
        )

    def _observation(self) -> Observation:
        return {
            "agent": {"row": self.position[0], "col": self.position[1]},
            "goal": {"row": self.goal[0], "col": self.goal[1]},
            "distance_to_goal": self._manhattan_distance(),
        }

    def _manhattan_distance(self) -> int:
        return abs(self.goal[0] - self.position[0]) + abs(self.goal[1] - self.position[1])


EnvironmentFactory = Callable[[], RLEnvironment]

