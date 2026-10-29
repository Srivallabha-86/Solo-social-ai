# Project Plan

## Goal

Provide solo founders with a dependable workflow for generating, organizing, and
tracking social media content.

## Backend MVP status

- FastAPI application with health checks and generated API documentation.
- Local caption generation by default, with optional OpenAI configuration.
- Persistent content ideas and weekly calendar posts backed by SQLAlchemy.
- Content and calendar create, list, filter, retrieve, update, and delete APIs.
- Request validation and automated tests using isolated temporary databases.
- SQLite initialization, local setup guidance, and persistent Docker storage.

## Deferred production work

1. Add Alembic migrations and a production database driver/configuration.
2. Add user authentication, ownership boundaries, and team permissions.
3. Implement background scheduling with retries and idempotent job handling.
4. Add opt-in integrations for publishing to LinkedIn, X, and Instagram.
5. Add operational logging, metrics, tracing, and deployment-specific health
   checks.
6. Build a user interface if a web dashboard is required.

External publishing needs platform developer applications, credentials, and
product decisions about approval and retry behavior. It is intentionally not
implemented in the MVP.
