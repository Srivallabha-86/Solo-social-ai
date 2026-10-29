# Project Plan

## Goal

Provide solo founders with a dependable workflow for generating, organizing, and
tracking social media content.

## Backend MVP status

- FastAPI application with health checks and generated API documentation.
- Local caption generation by default, with optional OpenAI configuration.
- Email/password authentication with short-lived signed bearer tokens.
- User-scoped content ideas and calendar posts backed by SQLAlchemy.
- SQLite development and PostgreSQL driver support.
- Alembic schema migrations, including safe retention of legacy unowned rows.
- Content and calendar create, list, filter, retrieve, update, and delete APIs.
- Request validation and automated tests using isolated temporary databases.
- SQLite initialization, local setup guidance, and persistent Docker storage.

## Deferred production work

1. Add email verification, password reset, rate limiting, and team permissions.
2. Implement background scheduling with retries and idempotent job handling.
3. Add opt-in integrations for publishing to LinkedIn, X, and Instagram.
4. Add operational logging, metrics, tracing, and deployment-specific health
   checks.
5. Harden deployment with TLS termination, secret management, backups, and
   restore procedures.

External publishing needs platform developer applications, credentials, and
product decisions about approval and retry behavior. It is intentionally not
implemented yet. Calendar entries can be scheduled in the database, but no
worker automatically sends them to a platform.
