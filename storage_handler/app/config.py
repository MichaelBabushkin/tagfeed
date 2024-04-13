from pydantic_settings import BaseSettings, SettingsConfigDict

folder = "storage_handler"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{folder}/.env.app", env_file_encoding="utf-8"
    )

    storage_handler_port: str
    app_folder: str


class PublicSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{folder}/.env", env_file_encoding="utf-8"
    )
    app_data_folder: str


app_settings = AppSettings()
public_settings = PublicSettings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")


settings = Settings(**{**AppSettings().model_dump(), **PublicSettings().model_dump()})
