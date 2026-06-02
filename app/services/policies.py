from random import Random

from app.domain.environments import Action, Observation
from app.domain.schemas import PolicyName


class PolicyEngine:
    def choose_action(
        self,
        policy: PolicyName,
        observation: Observation,
        action_space: list[Action],
        random: Random,
    ) -> Action:
        if policy == PolicyName.random:
            return random.choice(action_space)
        if policy == PolicyName.greedy:
            return self._greedy_action(observation)
        msg = f"Unsupported policy: {policy}"
        raise ValueError(msg)

    def _greedy_action(self, observation: Observation) -> Action:
        agent = observation["agent"]
        goal = observation["goal"]
        if agent["row"] < goal["row"]:
            return "down"
        if agent["col"] < goal["col"]:
            return "right"
        if agent["row"] > goal["row"]:
            return "up"
        return "left"


policy_engine = PolicyEngine()

