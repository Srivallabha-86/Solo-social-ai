from __future__ import annotations

from google import genai
from google.genai.errors import APIError as GeminiAPIError
from openai import OpenAI
from openai import OpenAIError

from ai.ai_engine import AIEngine
from app.core.config import settings


class AIProviderConfigurationError(Exception):
    """Raised when an external AI provider is enabled without its credentials."""


class AIProviderResponseError(Exception):
    """Raised when a configured provider returns unusable content."""


class AIProviderRequestError(Exception):
    """Raised when a configured AI provider rejects or cannot process a request."""


class CaptionGenerationService:
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

        prompt = (
            f"Write a polished {platform} post for {audience} about {topic}. "
            "Include a useful, specific takeaway and a natural question or call "
            "to action. Return only the post copy."
        )
        if settings.ai_provider == "openai":
            if not settings.openai_api_key:
                raise AIProviderConfigurationError(
                    "AI_PROVIDER is set to 'openai' but OPENAI_API_KEY is not configured."
                )
            try:
                response = OpenAI(api_key=settings.openai_api_key).chat.completions.create(
                    model=settings.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                )
            except OpenAIError as exc:
                raise AIProviderRequestError(
                    "The OpenAI provider could not generate content."
                ) from exc
            result = response.choices[0].message.content
            caption = result.strip() if result else ""
        elif settings.ai_provider == "gemini":
            if not settings.gemini_api_key:
                raise AIProviderConfigurationError(
                    "AI_PROVIDER is set to 'gemini' but GEMINI_API_KEY is not configured."
                )
            try:
                response = genai.Client(
                    api_key=settings.gemini_api_key,
                ).models.generate_content(
                    model=settings.gemini_model,
                    contents=prompt,
                )
            except GeminiAPIError as exc:
                raise AIProviderRequestError(
                    "The Gemini provider could not generate content."
                ) from exc
            result = response.text
            caption = result.strip() if result else ""
        else:
            raise RuntimeError(f"Unsupported AI provider: {settings.ai_provider}")

        if not caption:
            raise AIProviderResponseError("The AI provider returned an empty caption.")
        return caption
