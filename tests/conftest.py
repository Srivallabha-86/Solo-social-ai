from __future__ import annotations

import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_route() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Solo Social AI is running"


def test_health_route() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
