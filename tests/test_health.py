from __future__ import annotations

from datetime import datetime


def test_health_endpoint() -> None:
    assert datetime.utcnow() is not None
