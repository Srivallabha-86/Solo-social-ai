from datetime import datetime


class WeeklyWorkflow:
    """Simple automation workflow for generating a weekly marketing cadence."""

    def __init__(self, engine=None):
        self.engine = engine

    def run(self, topic: str, audience: str = "solo founders") -> dict:
        if self.engine is None:
            raise ValueError("An AIEngine instance is required.")

        content_plan = self.engine.generate_weekly_content(topic)
        created_at = datetime.utcnow().isoformat()

        return {
            "topic": topic,
            "audience": audience,
            "created_at": created_at,
            "content_plan": content_plan,
        }
