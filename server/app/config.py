from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="server/.env.app", env_file_encoding="utf-8"
    )

    algorithm: str
    access_token_expire_minutes: int
    content_pending_expire_minutes: int


class PrivateSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="server/.env", env_file_encoding="utf-8")

    secret_key: str
    database_hostname: str
    database_name: str
    database_port: str
    database_username: str
    database_password: str
    storage_handler_hostname: str
    storage_handler_port: str

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
