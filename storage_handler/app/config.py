from pydantic_settings import BaseSettings

folder = "storage_handler"


class AppSettings(BaseSettings):
    storage_handler_port: str
    app_folder: str

    class Config:
        env_file = f"{folder}/.env.app"


class PublicSettings(BaseSettings):
    app_data_folder: str

    class Config:
        env_file = f"{folder}/.env"


app_settings = AppSettings()
public_settings = PublicSettings()


class Settings(BaseSettings):
    class Config:
        extra = "allow"


settings = Settings(**{**AppSettings().model_dump(), **PublicSettings().model_dump()})
