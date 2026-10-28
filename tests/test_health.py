from __future__ import annotations


def test_root_route(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Solo Social AI is running"


def test_health_route(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
