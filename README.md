# Solo Social AI

AI-powered weekly social media marketing assistant for solo founders.

This project helps founders plan, draft, and schedule weekly social media content with AI assistance. It combines a lightweight app shell, prompt-driven AI generation, automation workflow hooks, and a simple dashboard for content planning.

## Features

- AI-generated social media post concepts and captions
- Weekly content planning workflow
- Simple calendar dashboard for content scheduling
- Local SQLite database for storing generated ideas and posts
- Basic tests for AI prompt logic

## Project Structure

```text
solosocial-ai/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── app.py
├── ai/
│   ├── ai_engine.py
│   └── prompts.py
├── automation/
│   └── workflow.py
├── database/
│   └── database.py
├── dashboard/
│   └── content_calendar.py
├── tests/
│   └── test_ai_engine.py
├── docs/
│   └── project_plan.md
└── .env
```

## Quick start

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
4. Add your API keys to `.env`.
5. Run the app:
   ```bash
   python app.py
   ```

## Environment variables

- `OPENAI_API_KEY`: API key used by the AI engine.
- `DATABASE_PATH`: Optional custom SQLite path.

## Roadmap

- Add content generation prompts for LinkedIn, X, and Instagram
- Build a weekly planning workflow for founders
- Improve dashboard UI for monthly content plans
- Add scheduler support for publishing workflows

## License

This project is currently for internal prototype and experimentation.
