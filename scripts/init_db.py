from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base


def init_db() -> None:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./solo_social_ai.db")
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
