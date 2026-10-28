from __future__ import annotations

from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
