from pydantic_settings import BaseSettings, SettingsConfigDict


class GitHubSettings(BaseSettings):
    app_id: int = 0
    installation_id: int = 0
    private_key_base64: str = ""
    use_auth: bool = True

    model_config = SettingsConfigDict(
        env_prefix="GITHUB_",
        env_file=".env",
        extra="ignore",
    )
