from app.domain.environments import EnvironmentFactory, GridWorldEnvironment, RLEnvironment
from app.domain.schemas import EnvironmentInfo


class EnvironmentRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, EnvironmentFactory] = {}
        self.register(GridWorldEnvironment.info.id, GridWorldEnvironment)

    def register(self, environment_id: str, factory: EnvironmentFactory) -> None:
        self._factories[environment_id] = factory

    def list(self) -> list[EnvironmentInfo]:
        return [factory().info for factory in self._factories.values()]

    def get(self, environment_id: str) -> RLEnvironment | None:
        factory = self._factories.get(environment_id)
        return factory() if factory else None


environment_registry = EnvironmentRegistry()

