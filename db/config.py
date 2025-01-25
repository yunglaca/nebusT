from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # database
    db_port: int = Field(env="DB_PORT")  # type: ignore
    db_name: str = Field(env="DB_NAME")  # type: ignore
    db_user: str = Field(env="DB_USER")  # type: ignore
    db_host: str = Field(env="DB_HOST")  # type: ignore
    db_pass: str = Field(env="DB_PASS")  # type: ignore

    # apikey
    api_key: str = Field(env="API_KEY")  # type: ignore

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
