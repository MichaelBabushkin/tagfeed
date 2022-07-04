from pydantic import BaseSettings


class AppSettings(BaseSettings):
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env.app"


class PublicSettings(BaseSettings):
    database_hostname: str
    database_name: str
    database_port: str

    class Config:
        env_file = ".env"


class PrivateSettings(BaseSettings):
    database_username: str
    database_password: str
    secret_key: str

    class Config:
        env_file = ".env.private"


app_settings = AppSettings()
public_settings = PublicSettings()
private_settings = PrivateSettings()


class Settings(BaseSettings):
    class Config:
        extra = "allow"


settings = Settings(
    **{**AppSettings().dict(), **PublicSettings().dict(), **PrivateSettings().dict()}
)
