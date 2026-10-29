from __future__ import annotations

from types import SimpleNamespace

from app.core.config import settings
from app.services import openai_service
from app.services.openai_service import OpenAIService


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

    result = OpenAIService().generate_caption(
        topic="Building an audience",
        platform="linkedin",
        audience="solo founders",
    )

    assert result == "A useful founder post."
    assert request["model"] == settings.openai_model
    assert "Building an audience" in request["messages"][0]["content"]
