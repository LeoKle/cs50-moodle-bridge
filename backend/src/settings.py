from pydantic_settings import BaseSettings, SettingsConfigDict

from interfaces.resolver.github_setting import GitHubSettings
from repositories.mongo.mongo_settings import MongoSettings


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()
    github: GitHubSettings = GitHubSettings()

    model_config = SettingsConfigDict()


if __name__ == "__main__":
    settings = Settings()

    print(settings.mongo.uri)
    print(settings.mongo.database)
