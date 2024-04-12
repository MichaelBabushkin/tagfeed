from pydantic_settings import BaseSettings, SettingsConfigDict

from storage_handler.app.config import folder, AppSettings, PublicSettings

PublicSettings.model_config.update(env_file=f"{folder}/.env.test")

app_settings = AppSettings()
public_settings = PublicSettings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

settings = Settings(**{**AppSettings().model_dump(), **PublicSettings().model_dump()})
