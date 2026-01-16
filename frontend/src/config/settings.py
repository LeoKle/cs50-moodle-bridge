"""Application settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """API client configuration."""

    backend_url: str = "http://localhost:8000"
    timeout: int = 30
    api_key: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="API_",
        env_file=".env",
        extra="ignore",
    )


class AppSettings(BaseSettings):
    """Application-wide settings."""

    use_mock_services: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


# Singleton pattern
_api_settings: APISettings | None = None
_app_settings: AppSettings | None = None


def get_api_settings() -> APISettings:
    """Get API settings singleton."""
    global _api_settings
    if _api_settings is None:
        _api_settings = APISettings()
    return _api_settings


def get_app_settings() -> AppSettings:
    """Get app settings singleton."""
    global _app_settings
    if _app_settings is None:
        _app_settings = AppSettings()
    return _app_settings
