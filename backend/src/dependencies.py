from dependency_injector import containers, providers

from settings import Settings


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(Settings())


if __name__ == "__main__":
    container = DependencyContainer()
