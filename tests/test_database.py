from __future__ import annotations

from sqlalchemy import create_engine, inspect, text

from app.db.session import init_db
from app.core.config import settings


def test_init_db_migrates_a_fresh_database(tmp_path, monkeypatch) -> None:
    database_path = tmp_path / "initialized.db"
    monkeypatch.setattr(settings, "database_url", f"sqlite:///{database_path.as_posix()}")

    init_db()

    test_engine = create_engine(f"sqlite:///{database_path.as_posix()}")
    assert {"calendar_posts", "content_ideas"} <= set(
        inspect(test_engine).get_table_names()
    )
    assert "users" in inspect(test_engine).get_table_names()
    assert "owner_id" in {
        column["name"] for column in inspect(test_engine).get_columns("content_ideas")
    }
    test_engine.dispose()


def test_init_db_preserves_existing_content_tables(tmp_path, monkeypatch) -> None:
    database_path = tmp_path / "legacy.db"
    database_url = f"sqlite:///{database_path.as_posix()}"
    legacy_engine = create_engine(database_url)
    with legacy_engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE users ("
                "id INTEGER PRIMARY KEY, email VARCHAR(320) NOT NULL UNIQUE, "
                "password_hash VARCHAR(255) NOT NULL, created_at DATETIME NOT NULL)"
            )
        )
        connection.execute(
            text(
                "CREATE TABLE content_ideas ("
                "id INTEGER PRIMARY KEY, topic VARCHAR(255) NOT NULL, "
                "platform VARCHAR(50) NOT NULL, content TEXT NOT NULL, "
                "created_at DATETIME NOT NULL)"
            )
        )
        connection.execute(
            text(
                "CREATE TABLE calendar_posts ("
                "id INTEGER PRIMARY KEY, scheduled_date DATETIME NOT NULL, "
                "topic VARCHAR(255) NOT NULL, theme VARCHAR(100) NOT NULL, "
                "platform VARCHAR(50) NOT NULL, suggested_time VARCHAR(5) NOT NULL, "
                "status VARCHAR(20) NOT NULL, content TEXT, created_at DATETIME NOT NULL)"
            )
        )
        connection.execute(
            text(
                "INSERT INTO content_ideas "
                "(topic, platform, content, created_at) "
                "VALUES ('legacy topic', 'linkedin', 'legacy text', CURRENT_TIMESTAMP)"
            )
        )
    legacy_engine.dispose()
    monkeypatch.setattr(settings, "database_url", database_url)

    init_db()

    migrated_engine = create_engine(database_url)
    with migrated_engine.connect() as connection:
        row = connection.execute(
            text("SELECT topic, owner_id FROM content_ideas")
        ).one()
    assert row.topic == "legacy topic"
    assert row.owner_id is None
    migrated_engine.dispose()
