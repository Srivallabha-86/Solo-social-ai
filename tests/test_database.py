from __future__ import annotations

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL

from app.db.session import init_db


def test_init_db_creates_application_tables(tmp_path, monkeypatch) -> None:
    test_engine = create_engine(
        URL.create("sqlite", database=str(tmp_path / "initialized.db"))
    )
    monkeypatch.setattr("app.db.session.engine", test_engine)

    init_db()

    assert {"calendar_posts", "content_ideas"} <= set(
        inspect(test_engine).get_table_names()
    )
    test_engine.dispose()
