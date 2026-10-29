
from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.calendar import CalendarPost


class CalendarService:
    """Create a weekly social media content calendar."""

    THEMES = [
        "Educational tip",
        "Founder story",
        "Product update",
        "Audience engagement",
        "Promotional post",
        "How-to guide",
        "Weekly recap",
    ]

    PLATFORMS = [
        "linkedin",
        "instagram",
        "x",
        "linkedin",
        "instagram",
        "x",
        "linkedin",
    ]

    POSTING_TIMES = [
        "09:00",
        "12:00",
        "10:00",
        "17:00",
        "11:00",
        "14:00",
        "16:00",
    ]

    def __init__(self, db: Session):
        self.db = db

    def build_weekly_plan(
        self,
        topic: str,
        start_date: date | None = None,
    ) -> list[dict[str, str]]:
        """Build a seven-day plan starting on the selected date."""

        if not topic or len(topic.strip()) < 3:
            raise ValueError("Topic must contain at least 3 characters.")

        first_day = start_date or date.today()
        plan = []

        for offset in range(7):
            post_date = first_day + timedelta(days=offset)

            plan.append(
                {
                    "date": post_date.isoformat(),
                    "topic": f"{topic.strip()} - {self.THEMES[offset]}",
                    "theme": self.THEMES[offset],
                    "platform": self.PLATFORMS[offset],
                    "suggested_time": self.POSTING_TIMES[offset],
                    "status": "planned",
                }
            )

        return plan

    def create_weekly_plan(
        self,
        owner_id: int,
        topic: str,
        start_date: date | None = None,
    ) -> list[CalendarPost]:
        plan = self.build_weekly_plan(topic, start_date)
        posts = [
            CalendarPost(
                owner_id=owner_id,
                scheduled_date=datetime.combine(
                    date.fromisoformat(item["date"]),
                    time.min,
                    tzinfo=timezone.utc,
                ),
                topic=item["topic"],
                theme=item["theme"],
                platform=item["platform"],
                suggested_time=item["suggested_time"],
                status=item["status"],
            )
            for item in plan
        ]
        self.db.add_all(posts)
        self.db.commit()
        for post in posts:
            self.db.refresh(post)
        return posts

    def create_post(
        self,
        owner_id: int,
        post_date: date,
        topic: str,
        theme: str,
        platform: str,
        suggested_time: time,
        content: str | None,
    ) -> CalendarPost:
        post = CalendarPost(
            owner_id=owner_id,
            scheduled_date=datetime.combine(
                post_date,
                time.min,
                tzinfo=timezone.utc,
            ),
            topic=topic,
            theme=theme,
            platform=platform,
            suggested_time=suggested_time.strftime("%H:%M"),
            status="planned",
            content=content,
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def list_posts(
        self,
        owner_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[CalendarPost]:
        statement = (
            select(CalendarPost)
            .where(CalendarPost.owner_id == owner_id)
            .order_by(CalendarPost.scheduled_date, CalendarPost.id)
        )
        if start_date is not None:
            start = datetime.combine(start_date, time.min, tzinfo=timezone.utc)
            statement = statement.where(CalendarPost.scheduled_date >= start)
        if end_date is not None:
            end = datetime.combine(
                end_date + timedelta(days=1),
                time.min,
                tzinfo=timezone.utc,
            )
            statement = statement.where(CalendarPost.scheduled_date < end)
        if status is not None:
            statement = statement.where(CalendarPost.status == status)
        statement = statement.offset(offset).limit(limit)
        return list(self.db.scalars(statement).all())

    def get_post(self, owner_id: int, post_id: int) -> CalendarPost | None:
        return self.db.scalar(
            select(CalendarPost).where(
                CalendarPost.id == post_id,
                CalendarPost.owner_id == owner_id,
            )
        )

    def update_post(
        self,
        post: CalendarPost,
        changes: dict[str, object],
    ) -> CalendarPost:
        for field, value in changes.items():
            if field == "date" and isinstance(value, date):
                value = datetime.combine(value, time.min, tzinfo=timezone.utc)
                field = "scheduled_date"
            elif field == "suggested_time" and isinstance(value, time):
                value = value.strftime("%H:%M")
            setattr(post, field, value)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_post(self, post: CalendarPost) -> None:
        self.db.delete(post)
        self.db.commit()
