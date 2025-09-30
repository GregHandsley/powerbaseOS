from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Base
    ENV: str = Field(default="dev")
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)

    # Postgres
    PG_HOST: str = Field(default="db")
    PG_PORT: int = Field(default=5432)
    PG_DB: str = Field(default="powerbase")
    PG_USER: str = Field(default="powerbase")
    PG_PASSWORD: str = Field(default="powerbase")

    # Sentry optional (unused here but in .env)
    SENTRY_DSN: str | None = None

    model_config = SettingsConfigDict(env_file="../../.env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_url_async(self) -> str:
        # asyncpg driver for SQLAlchemy
        return (
            f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}"
            f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        )

    @property
    def database_url_sync(self) -> str:
        # sync driver for Alembic offline or other tooling
        return (
            f"postgresql://{self.PG_USER}:{self.PG_PASSWORD}"
            f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()