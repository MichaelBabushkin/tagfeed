from pydantic import BaseSettings

from app.config import AppSettings, PublicSettings, PrivateSettings

PublicSettings.Config.env_file = ".env.test"
PrivateSettings.Config.env_file = ".env.private.test"

app_settings = AppSettings()
public_settings = PublicSettings()
private_settings = PrivateSettings()


class Settings(BaseSettings):
    class Config:
        extra = "allow"


settings = Settings(
    **{**AppSettings().dict(), **PublicSettings().dict(), **PrivateSettings().dict()}
)
