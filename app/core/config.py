from __future__ import annotations

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Solo Social AI"
    app_env: str = "dev"
    app_debug: bool = False
    database_url: str = "sqlite:///./solo_social_ai.db"
    ai_provider: Literal["local", "openai"] = "local"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"


settings = Settings()
