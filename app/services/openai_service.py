from __future__ import annotations

import os

from openai import OpenAI

from app.core.config import settings


class OpenAIService:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.client = OpenAI(api_key=api_key or settings.openai_api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model or settings.openai_model

    def generate_caption(self, topic: str, platform: str = "linkedin") -> str:
        if not self.client.api_key:
            return (
                f"Draft {platform} post for: {topic}. "
                "Share a practical lesson, explain a framework, and invite your audience to respond."
            )

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": f"Write a polished {platform} post about: {topic}",
                }
            ],
        )
        return response.output_text
