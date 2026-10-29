
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ContentIdea(Base):
    __tablename__ = "content_ideas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    topic: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="linkedin",
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    owner: Mapped[User | None] = relationship(back_populates="content_ideas")


from app.models.user import User
