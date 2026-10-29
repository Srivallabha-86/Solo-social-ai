from __future__ import annotations

import secrets
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
    ai_provider: Literal["local", "openai", "gemini"] = "local"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    livekit_url: str = ""
    livekit_api_key: str = ""
    livekit_api_secret: str = ""
    app_secret_key: str = ""
    access_token_expire_minutes: int = 30
    app_auto_migrate: bool = True

    def token_secret(self) -> str:
        if self.app_secret_key:
            return self.app_secret_key
        if self.app_env.lower() in {"prod", "production"}:
            raise RuntimeError("APP_SECRET_KEY must be configured in production.")
        return _development_secret


_development_secret = secrets.token_urlsafe(32)
settings = Settings()
