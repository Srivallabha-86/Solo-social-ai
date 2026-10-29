from __future__ import annotations

from openai import OpenAI

from ai.ai_engine import AIEngine
from app.core.config import settings


class AIProviderConfigurationError(Exception):
    """Raised when an external AI provider is enabled without its credentials."""


class AIProviderResponseError(Exception):
    """Raised when a configured provider returns unusable content."""


class OpenAIService:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model

    def generate_caption(
        self,
        topic: str,
        platform: str = "linkedin",
        audience: str = "solo founders",
    ) -> str:
        if settings.ai_provider == "local":
            return AIEngine().build_post_copy(
                topic,
                audience=audience,
                platform=platform,
            )

        if not self.api_key:
            raise AIProviderConfigurationError(
                "AI_PROVIDER is set to 'openai' but OPENAI_API_KEY is not configured."
            )

        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Write a polished {platform} post for {audience} about "
                        f"{topic}. Include a useful, specific takeaway and a natural "
                        "question or call to action. Return only the post copy."
                    ),
                }
            ],
        )

        caption = response.choices[0].message.content
        caption = caption.strip() if caption is not None else ""
        if not caption:
            raise AIProviderResponseError("The AI provider returned an empty caption.")
        return caption
