# Solo Social AI

AI-powered weekly social media marketing assistant for solo founders.

## Overview

Solo Social AI helps founders plan and generate social media content for their weekly marketing cadence. The system is structured for real-world use with an API layer, configuration management, content services, database access, and test coverage.

## Production-ready project structure

```text
solosocial-ai/
├── .gitignore
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md
├── pyproject.toml
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       └── content.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── content.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── content.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── content_service.py
│   │   ├── calendar_service.py
│   │   └── openai_service.py
│   └── utils/
│       └── __init__.py
├── scripts/
│   └── init_db.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_health.py
├── docs/
│   └── project_plan.md
└── .env
```

## Stack

- FastAPI for the API layer
- SQLAlchemy for persistence
- Pydantic for validation
- OpenAI integration for content generation
- SQLite by default for local development
- pytest for automated testing

## Getting started

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

4. Start the application:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Visit the API docs:

   - http://localhost:8000/docs
   - http://localhost:8000/redoc

## Environment variables

- `APP_NAME` — application name
- `APP_ENV` — environment (`dev`, `prod`, `test`)
- `APP_DEBUG` — debug mode
- `DATABASE_URL` — database connection string
- `OPENAI_API_KEY` — OpenAI API key
- `OPENAI_MODEL` — default model used for generation

## Development commands

```bash
make install
make test
make run
make format
```

## Production notes

- Use PostgreSQL in production instead of SQLite.
- Store secrets in environment variables and a secret manager.
- Enable structured logging and health checks.
- Add DB migrations with Alembic for schema management.

## License

This project is intended for internal and commercial experimentation by solo founders.
