from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_project_root(marker="pyproject.toml"):
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / marker).exists():
            return parent
    msg = f"Could not find {marker} in any parent directory."
    raise FileNotFoundError(msg)


ROOT_DIR = find_project_root()
load_dotenv(ROOT_DIR / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict()
