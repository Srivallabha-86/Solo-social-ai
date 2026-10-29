from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.content import ContentIdea


class ContentService:
    def __init__(self, db: Session):
        self.db = db

    def create_content_idea(
        self,
        owner_id: int,
        topic: str,
        platform: str,
        content: str,
    ) -> ContentIdea:
        idea = ContentIdea(
            owner_id=owner_id,
            topic=topic,
            platform=platform,
            content=content,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(idea)
        self.db.commit()
        self.db.refresh(idea)
        return idea

    def list_content_ideas(
        self,
        owner_id: int,
        platform: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[ContentIdea]:
        statement = (
            select(ContentIdea)
            .where(ContentIdea.owner_id == owner_id)
            .order_by(ContentIdea.id.desc())
        )
        if platform is not None:
            statement = statement.where(ContentIdea.platform == platform)
        statement = statement.offset(offset).limit(limit)
        return list(self.db.scalars(statement).all())

    def get_content_idea(self, owner_id: int, content_id: int) -> ContentIdea | None:
        return self.db.scalar(
            select(ContentIdea).where(
                ContentIdea.id == content_id,
                ContentIdea.owner_id == owner_id,
            )
        )

    def update_content_idea(
        self,
        idea: ContentIdea,
        changes: dict[str, str],
    ) -> ContentIdea:
        for field, value in changes.items():
            setattr(idea, field, value)
        self.db.commit()
        self.db.refresh(idea)
        return idea

    def delete_content_idea(self, idea: ContentIdea) -> None:
        self.db.delete(idea)
        self.db.commit()
