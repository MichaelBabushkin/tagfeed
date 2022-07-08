from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config import AppSettings, PublicSettings, PrivateSettings

PublicSettings.model_config["env_file"] = "server/.env.test"
PrivateSettings.model_config["env_file"] = "server/.env.private.test"

app_settings = AppSettings()
public_settings = PublicSettings()
private_settings = PrivateSettings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='allow', env_file_encoding='utf-8')


settings = Settings(
    **{**AppSettings().model_dump(), **PublicSettings().model_dump(), **PrivateSettings().model_dump()}
)
