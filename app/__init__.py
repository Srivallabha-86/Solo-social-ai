from __future__ import annotations

from typing import Any

from fastapi import FastAPI


def create_app() -> FastAPI:
    from app.main import app

    return app
