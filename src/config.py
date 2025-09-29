from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_username: str
    database_password: str
    database_port: str
    database_host: str
    database_name: str

    class Config:
        env_file = ".env"

setting = Settings()
