from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    content_ideas: Mapped[list[ContentIdea]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    calendar_posts: Mapped[list[CalendarPost]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )


from app.models.calendar import CalendarPost
from app.models.content import ContentIdea
