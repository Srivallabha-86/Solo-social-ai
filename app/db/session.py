from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    echo=settings.app_debug,
    connect_args=(
        {"check_same_thread": False}
        if settings.database_url.startswith("sqlite")
        else {}
    ),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Apply database migrations to the configured database."""
    import app.models  # noqa: F401

    migration_config = Config(str(Path(__file__).resolve().parents[2] / "alembic.ini"))
    command.upgrade(migration_config, "head")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
