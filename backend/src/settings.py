from pydantic_settings import BaseSettings, SettingsConfigDict

from repositories.mongo.mongo_settings import MongoSettings


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()

    model_config = SettingsConfigDict()


if __name__ == "__main__":
    settings = Settings()

    print(settings.mongo.uri)
    print(settings.mongo.database)
