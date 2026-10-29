
from __future__ import annotations

from app.core.config import settings

def test_create_content_idea(client) -> None:
    response = client.post(
        "/api/v1/content",
        json={
            "topic": "Social media marketing",
            "platform": "linkedin",
            "content": "Three tips to improve social media engagement.",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["topic"] == "Social media marketing"
    assert data["platform"] == "linkedin"
    assert data["content"] == "Three tips to improve social media engagement."
    assert "id" in data
    assert "created_at" in data


def test_list_content_ideas(client) -> None:
    response = client.get("/api/v1/content")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_generate_content_saves_generated_draft(client) -> None:
    response = client.post(
        "/api/v1/content/generate",
        json={
            "topic": "Building an audience",
            "platform": "linkedin",
            "audience": "independent founders",
        },
    )

    assert response.status_code == 201
    content = response.json()
    assert content["topic"] == "Building an audience"
    assert content["platform"] == "linkedin"
    assert content["content"]
    assert client.get(f"/api/v1/content/{content['id']}").json() == content


def test_content_crud_and_platform_filter(client) -> None:
    created = client.post(
        "/api/v1/content",
        json={
            "topic": "Email marketing",
            "platform": "x",
            "content": "A short, useful post about email marketing.",
        },
    ).json()

    updated = client.patch(
        f"/api/v1/content/{created['id']}",
        json={"topic": "Better email marketing"},
    )
    assert updated.status_code == 200
    assert updated.json()["topic"] == "Better email marketing"
    assert len(client.get("/api/v1/content?platform=x").json()) == 1
    assert client.get("/api/v1/content?platform=instagram").json() == []

    deleted = client.delete(f"/api/v1/content/{created['id']}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/content/{created['id']}").status_code == 404


def test_content_rejects_empty_patch(client) -> None:
    created = client.post(
        "/api/v1/content",
        json={
            "topic": "Email marketing",
            "content": "A short, useful post about email marketing.",
        },
    ).json()

    response = client.patch(f"/api/v1/content/{created['id']}", json={})
    assert response.status_code == 422


def test_openai_mode_requires_an_api_key(client, monkeypatch) -> None:
    monkeypatch.setattr(settings, "ai_provider", "openai")
    monkeypatch.setattr(settings, "openai_api_key", "")

    response = client.post(
        "/api/v1/content/generate",
        json={"topic": "Building an audience"},
    )
    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]


def test_gemini_mode_requires_an_api_key(client, monkeypatch) -> None:
    monkeypatch.setattr(settings, "ai_provider", "gemini")
    monkeypatch.setattr(settings, "gemini_api_key", "")

    response = client.post(
        "/api/v1/content/generate",
        json={"topic": "Building an audience"},
    )
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]
