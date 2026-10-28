import os
import sqlite3
from typing import Any, Dict, List


class DatabaseManager:
    """Basic SQLite helper for storing generated content ideas."""

    def __init__(self, database_path: str | None = None):
        self.database_path = database_path or os.getenv("DATABASE_PATH", "./data/solo_social_ai.db")
        os.makedirs(os.path.dirname(self.database_path) or ".", exist_ok=True)
        self._initialize_db()

    def _initialize_db(self) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS content_ideas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    idea TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_idea(self, topic: str, idea: str) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                "INSERT INTO content_ideas (topic, idea) VALUES (?, ?)",
                (topic, idea),
            )

    def get_ideas(self, topic: str | None = None) -> List[Dict[str, Any]]:
        query = "SELECT id, topic, idea, created_at FROM content_ideas"
        params: List[Any] = []

        if topic is not None:
            query += " WHERE topic = ?"
            params.append(topic)

        query += " ORDER BY created_at DESC"

        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute(query, params).fetchall()

        return [
            {"id": row[0], "topic": row[1], "idea": row[2], "created_at": row[3]}
            for row in rows
        ]
