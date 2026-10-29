
from __future__ import annotations

from datetime import date, timedelta


def test_create_weekly_calendar(client) -> None:
    start_date = date(2026, 11, 2)

    response = client.post(
        "/api/v1/calendar/weekly",
        json={
            "topic": "Social media marketing",
            "start_date": start_date.isoformat(),
        },
    )

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 7
    assert posts[0]["date"] == start_date.isoformat()
    assert posts[-1]["date"] == (
        start_date + timedelta(days=6)
    ).isoformat()
    assert posts[0]["platform"] == "linkedin"
    assert posts[0]["status"] == "planned"


def test_weekly_calendar_rejects_short_topic(client) -> None:
    response = client.post(
        "/api/v1/calendar/weekly",
        json={"topic": "AI"},
    )

    assert response.status_code == 422


def test_calendar_posts_are_persisted_and_manageable(client) -> None:
    start_date = date(2026, 11, 2)
    created = client.post(
        "/api/v1/calendar/weekly",
        json={
            "topic": "Content strategy",
            "start_date": start_date.isoformat(),
        },
    )
    assert created.status_code == 200
    first_post = created.json()[0]
    assert first_post["id"]

    listed = client.get(
        f"/api/v1/calendar?start_date={start_date.isoformat()}"
        f"&end_date={(start_date + timedelta(days=6)).isoformat()}"
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 7

    updated = client.patch(
        f"/api/v1/calendar/{first_post['id']}",
        json={"status": "draft", "content": "Draft copy for review."},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "draft"
    assert updated.json()["content"] == "Draft copy for review."

    filtered = client.get("/api/v1/calendar?status=draft")
    assert len(filtered.json()) == 1

    deleted = client.delete(f"/api/v1/calendar/{first_post['id']}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/calendar/{first_post['id']}").status_code == 404


def test_calendar_rejects_invalid_date_range(client) -> None:
    response = client.get(
        "/api/v1/calendar?start_date=2026-11-03&end_date=2026-11-02"
    )
    assert response.status_code == 422
