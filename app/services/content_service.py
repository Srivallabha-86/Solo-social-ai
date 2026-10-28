from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.content import ContentIdea


class ContentService:
    def __init__(self, db: Session):
        self.db = db

    def create_content_idea(self, topic: str, platform: str, content: str) -> ContentIdea:
        idea = ContentIdea(
            topic=topic,
            platform=platform,
            content=content,
            created_at=datetime.utcnow(),
        )
        self.db.add(idea)
        self.db.commit()
        self.db.refresh(idea)
        return idea

    def list_content_ideas(self) -> list[ContentIdea]:
        return self.db.query(ContentIdea).order_by(ContentIdea.id.desc()).all()
