from __future__ import annotations

from collections.abc import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.db.session import Base
from app.main import create_app


@pytest.fixture
def client(tmp_path) -> Generator[TestClient, None, None]:
    test_engine = create_engine(
        URL.create("sqlite", database=str(tmp_path / "test.db")),
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    application = create_app(initialize_database=False)

    def override_get_db() -> Generator:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    application.dependency_overrides[get_db] = override_get_db
    with TestClient(application) as test_client:
        registration = test_client.post(
            "/api/v1/auth/register",
            json={
                "email": "demo@example.com",
                "password": "demo-founder-password",
            },
        )
        assert registration.status_code == 201
        test_client.headers["Authorization"] = (
            f"Bearer {registration.json()['access_token']}"
        )
        yield test_client
    application.dependency_overrides.clear()
    test_engine.dispose()
