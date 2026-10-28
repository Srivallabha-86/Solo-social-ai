
from __future__ import annotations


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
