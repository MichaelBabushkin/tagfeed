from pydantic_settings import BaseSettings

from storage_handler.app.config import folder, AppSettings, PublicSettings

PublicSettings.Config.env_file = f"{folder}/.env.test"

app_settings = AppSettings()
public_settings = PublicSettings()


class Settings(BaseSettings):
    class Config:
        extra = "allow"


settings = Settings(**{**AppSettings().model_dump(), **PublicSettings().model_dump()})
