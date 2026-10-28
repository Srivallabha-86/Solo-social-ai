
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
