# ./src/back_end/src/engine/settings.py
"""Settings module, this is only loaded once when the application starts.

Holds important info used throughout the app.
"""

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

HERE = Path(
    __file__
).resolve()  # /workspace/src/back_end/src/engine/settings.py
WORKSPACE = HERE.parents[4]
DOT_ENV_PATH = WORKSPACE / ".env"


class DatabaseSettings(BaseModel):
    """BaseModel containing basic database settings."""

    url: str = "sqlite+aiosqlite:///./data.db"  # Default value


class SecuritySettings(BaseModel):
    """Settings for signing session tokens."""

    # Dev-only default. Override in production via SECURITY__SECRET_KEY so the
    # signing key is not a value that lives in the source tree.
    secret_key: str = "dev-only-insecure-secret-change-me"


class Settings(BaseSettings):
    """Settings python object, loaded once, used throughout the application."""

    model_config = SettingsConfigDict(
        env_file=DOT_ENV_PATH, env_nested_delimiter="__", extra="ignore"
    )
    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()


app_settings = Settings()

if __name__ == "__main__":
    print(HERE)
    print(WORKSPACE)
