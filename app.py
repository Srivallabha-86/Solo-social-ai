import os
from dotenv import load_dotenv

from ai.ai_engine import AIEngine

load_dotenv()


def main() -> None:
    """Run a simple interactive demo for the AI social assistant."""
    print("Solo Social AI")
    print("================")

    engine = AIEngine()
    topic = "Productivity habits for solo founders"
    result = engine.generate_weekly_content(topic)

    print(f"\nTopic: {topic}\n")
    print(result)


if __name__ == "__main__":
    main()
