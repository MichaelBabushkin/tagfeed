from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config import AppSettings, PrivateSettings

PrivateSettings.model_config["env_file"] = "server/.env.test"

app_settings = AppSettings()
private_settings = PrivateSettings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow", env_file_encoding="utf-8")


settings = Settings(
    **{
        **AppSettings().model_dump(),
        **PrivateSettings().model_dump(),
    }
)
