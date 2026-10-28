from __future__ import annotations

from fastapi.testclient import TestClient

import pytest

from app.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)
