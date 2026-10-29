import os


class AIEngine:
    """Generates content ideas and prompts for founder social marketing."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def generate_weekly_content(self, topic: str) -> str:
        """Create a weekly content plan for a given topic."""
        ideas = [
            f"1. Share a founder lesson on {topic}",
            f"2. Explain a practical framework for {topic}",
            f"3. Post a short tactical tip linked to {topic}",
            f"4. Create a behind-the-scenes story about building with {topic}",
            f"5. End with a CTA asking your audience about their biggest challenge with {topic}",
        ]
        return "\n".join(ideas)

    def build_post_copy(
        self,
        message: str,
        audience: str = "founders",
        platform: str = "linkedin",
    ) -> str:
        """Create a useful local sample caption for the selected platform."""
        if platform == "x":
            return (
                f"Building for {audience} means solving one real problem at a time.\n\n"
                f"This week: {message}. Small, useful improvements beat trying to do "
                "everything at once.\n\n"
                "What are you working on next?"
            )

        if platform == "instagram":
            return (
                f"A small founder reminder for anyone building for {audience}:\n\n"
                f"{message}\n\n"
                "Listen closely. Make one useful improvement. Share what you learn.\n\n"
                "What are you working on this week? 👇"
            )

        return (
            f"One thing I’m learning while building for {audience}: {message}.\n\n"
            "The best progress often comes from focusing on one real customer problem, "
            "making a small improvement, and sharing what you learn along the way.\n\n"
            "What is the one thing you are optimizing for this week?"
        )
