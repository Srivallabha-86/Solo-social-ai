from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_root_route(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Your next week" in response.text


def test_health_route(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_application_initializes_database_on_startup(monkeypatch) -> None:
    initialized = False

    def mark_initialized() -> None:
        nonlocal initialized
        initialized = True

    monkeypatch.setattr("app.main.init_db", mark_initialized)

    with TestClient(create_app()):
        assert initialized
