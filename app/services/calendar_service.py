from __future__ import annotations

from datetime import datetime, timedelta


class CalendarService:
    def build_weekly_plan(self, topic: str) -> list[dict[str, str]]:
        today = datetime.utcnow().date()
        plan = []
        for offset in range(5):
            date = today + timedelta(days=offset)
            plan.append(
                {
                    "date": date.isoformat(),
                    "topic": topic,
                    "platform": "linkedin",
                    "status": "planned",
                }
            )
        return plan
