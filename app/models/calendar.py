
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class CalendarPost(Base):
    __tablename__ = "calendar_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    scheduled_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    topic: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    theme: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="linkedin",
    )

    suggested_time: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        default="09:00",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="planned",
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    owner: Mapped[User | None] = relationship(back_populates="calendar_posts")


from app.models.user import User
