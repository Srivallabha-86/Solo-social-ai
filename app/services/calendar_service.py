
from datetime import date, timedelta


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

