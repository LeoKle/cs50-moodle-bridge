from pathlib import Path

from dependency_injector import containers, providers
from dotenv import load_dotenv

from settings import Settings


def find_project_root(marker="pyproject.toml"):
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / marker).exists():
            return parent
    msg = f"Could not find {marker} in any parent directory."
    raise FileNotFoundError(msg)


ROOT_DIR = find_project_root()
load_dotenv(ROOT_DIR / ".env")


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_pydantic(Settings())


if __name__ == "__main__":
    container = DependencyContainer()
