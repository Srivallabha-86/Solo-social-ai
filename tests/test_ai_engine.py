import pytest

from ai.ai_engine import AIEngine


def test_generate_weekly_content_returns_five_ideas():
    engine = AIEngine(api_key="test-key")
    result = engine.generate_weekly_content("building a product")

    items = [line for line in result.splitlines() if line.strip()]
    assert len(items) == 5
    assert all(item.startswith(("1.", "2.", "3.", "4.", "5.")) for item in items)


def test_build_post_copy_contains_message_and_cta():
    engine = AIEngine(api_key="test-key")
    result = engine.build_post_copy("Ship in public.")

    assert "Ship in public." in result
    assert "What is the one thing you are optimizing for this week?" in result


def test_build_post_copy_adapts_to_x():
    result = AIEngine().build_post_copy(
        "Improving onboarding",
        audience="independent founders",
        platform="x",
    )

    assert "Improving onboarding" in result
    assert "independent founders" in result
    assert "What are you working on next?" in result
