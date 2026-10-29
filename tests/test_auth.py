from __future__ import annotations

import pytest

from app.core.config import settings


def test_registration_login_and_me(client) -> None:
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "email": "founder@example.com",
            "password": "strong-founder-password",
        },
    )
    assert registration.status_code == 201
    token = registration.json()["access_token"]
    assert registration.json()["user"]["email"] == "founder@example.com"

    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "FOUNDER@example.com",
            "password": "strong-founder-password",
        },
    )
    assert login.status_code == 200
    assert login.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"
    current_user = client.get("/api/v1/auth/me")
    assert current_user.status_code == 200
    assert current_user.json()["email"] == "founder@example.com"


def test_invalid_and_duplicate_authentication(client) -> None:
    duplicate = client.post(
        "/api/v1/auth/register",
        json={
            "email": "DEMO@example.com",
            "password": "strong-founder-password",
        },
    )
    assert duplicate.status_code == 409

    bad_login = client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com", "password": "wrong-password"},
    )
    assert bad_login.status_code == 401


def test_content_api_requires_authentication(client) -> None:
    authorization = client.headers.pop("Authorization")
    try:
        response = client.get("/api/v1/content")
    finally:
        client.headers["Authorization"] = authorization

    assert response.status_code == 401


def test_users_cannot_read_each_others_content(client) -> None:
    content = client.post(
        "/api/v1/content",
        json={
            "topic": "Founder audience",
            "content": "A useful and practical founder update.",
        },
    ).json()
    second_account = client.post(
        "/api/v1/auth/register",
        json={
            "email": "another@example.com",
            "password": "another-strong-password",
        },
    )
    assert second_account.status_code == 201

    client.headers["Authorization"] = (
        f"Bearer {second_account.json()['access_token']}"
    )
    assert client.get("/api/v1/content").json() == []
    assert client.get(f"/api/v1/content/{content['id']}").status_code == 404


def test_production_requires_configured_signing_secret(monkeypatch) -> None:
    monkeypatch.setattr(settings, "app_env", "production")
    monkeypatch.setattr(settings, "app_secret_key", "")

    with pytest.raises(RuntimeError, match="APP_SECRET_KEY"):
        settings.token_secret()
