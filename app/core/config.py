from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = "Solo Social AI"
    app_env: str = "dev"
    app_debug: bool = False
    database_url: str = "sqlite:///./solo_social_ai.db"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"


settings = Settings()
