import os
from typing import List, Dict


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

    def build_post_copy(self, message: str, audience: str = "founders") -> str:
        """Return a brief social media caption based on the message."""
        return (
            f"Here is a draft for {audience}:\n"
            f"\n{message}\n\n"
            f"What is the one thing you are optimizing for this week?"
        )
