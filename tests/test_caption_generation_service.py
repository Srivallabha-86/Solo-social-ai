from __future__ import annotations

from types import SimpleNamespace

import pytest
from google.genai.errors import APIError as GeminiAPIError

from app.core.config import settings
from app.services import openai_service
from app.services.openai_service import (
    AIProviderRequestError,
    AIProviderResponseError,
    CaptionGenerationService,
)


def test_openai_service_formats_and_cleans_provider_response(monkeypatch) -> None:
    request: dict[str, object] = {}

    def create_completion(**kwargs):
        request.update(kwargs)
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="  A useful founder post.  ")
                )
            ]
        )

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=create_completion),
        )
    )
    monkeypatch.setattr(settings, "ai_provider", "openai")
    monkeypatch.setattr(settings, "openai_api_key", "test-key")
    monkeypatch.setattr(openai_service, "OpenAI", lambda api_key: fake_client)

    result = CaptionGenerationService().generate_caption(
        topic="Building an audience",
        platform="linkedin",
        audience="solo founders",
    )

    assert result == "A useful founder post."
    assert request["model"] == settings.openai_model
    assert "Building an audience" in request["messages"][0]["content"]


def test_gemini_service_formats_and_cleans_provider_response(monkeypatch) -> None:
    request: dict[str, object] = {}

    def generate_content(**kwargs):
        request.update(kwargs)
        return SimpleNamespace(text="  A Gemini founder post.  ")

    fake_client = SimpleNamespace(
        models=SimpleNamespace(generate_content=generate_content),
    )
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    monkeypatch.setattr(settings, "gemini_api_key", "test-key")
    monkeypatch.setattr(openai_service.genai, "Client", lambda api_key: fake_client)

    result = CaptionGenerationService().generate_caption(
        topic="Building an audience",
        platform="linkedin",
        audience="solo founders",
    )

    assert result == "A Gemini founder post."
    assert request["model"] == settings.gemini_model
    assert "Building an audience" in request["contents"]


def test_gemini_service_rejects_empty_response(monkeypatch) -> None:
    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda **kwargs: SimpleNamespace(text="  "),
        )
    )
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    monkeypatch.setattr(settings, "gemini_api_key", "test-key")
    monkeypatch.setattr(openai_service.genai, "Client", lambda api_key: fake_client)

    with pytest.raises(AIProviderResponseError, match="empty caption"):
        CaptionGenerationService().generate_caption(topic="Building an audience")


def test_gemini_service_wraps_provider_api_errors(monkeypatch) -> None:
    def generate_content(**kwargs):
        raise GeminiAPIError(500, {"error": {"message": "provider failure"}})

    fake_client = SimpleNamespace(
        models=SimpleNamespace(generate_content=generate_content),
    )
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    monkeypatch.setattr(settings, "gemini_api_key", "test-key")
    monkeypatch.setattr(openai_service.genai, "Client", lambda api_key: fake_client)

    with pytest.raises(AIProviderRequestError, match="Gemini provider"):
        CaptionGenerationService().generate_caption(topic="Building an audience")
