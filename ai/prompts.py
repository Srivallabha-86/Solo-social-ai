SOCIAL_POST_TEMPLATE = """
You are an experienced social media strategist for solo founders.
Create a weekly content plan around the topic: {topic}.

Requirements:
- Include 5 post ideas
- Use a clear founder-friendly tone
- Mix educational, personal, and CTA-based content
- Keep each idea concise and actionable
"""

CONTENT_PROMPTS = {
    "linkedin": "Write a professional founder-focused LinkedIn post about {topic}.",
    "x": "Write a short, punchy X thread about {topic}.",
    "instagram": "Write an Instagram caption and carousel hook for {topic}.",
}
