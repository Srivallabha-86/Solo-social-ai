# Solo Social AI

Solo Social AI is a backend MVP for planning a week of social content, drafting
platform-specific captions, and managing saved content and calendar posts.

## Features

- FastAPI endpoints for health checks, content ideas, and calendar posts.
- A browser dashboard at `/` for solo founders to draft a post and plan a week.
- Email/password registration and login with short-lived bearer access tokens.
- Per-user ownership for content and calendar API operations.
- Local caption generation by default; optional OpenAI or Gemini generation via
  environment configuration.
- SQLite persistence for local development and PostgreSQL support for deployments.
- Content and calendar listing, filtering, updates, and deletion.
- Alembic migrations for new and existing databases.
- Request validation and automated API/service tests.

Live social publishing and automatic background posting are not enabled. The
calendar API stores scheduled content; it does not dispatch posts to social
platforms.

## Requirements

- Python 3.11 or newer
- pip

## Run locally (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

Open the founder dashboard at <http://127.0.0.1:8000/> and the interactive API
docs at <http://127.0.0.1:8000/docs>. The health check is available at
<http://127.0.0.1:8000/health>.

By default, the app uses local generation and creates `solo_social_ai.db` in the
working directory. No AI API key is required for local generation. On first
startup, local mode applies Alembic migrations automatically. Use a unique
`APP_SECRET_KEY` in `.env`; development can start without one, but tokens expire
when the development process restarts.

## Authenticated API

Create a user from the dashboard or through the API. Passwords must be at least
12 characters. Registration and login return a short-lived bearer token:

```powershell
$account = Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/auth/register `
  -ContentType "application/json" `
  -Body '{"email":"founder@example.com","password":"a-long-demo-password"}'

$headers = @{ Authorization = "Bearer $($account.access_token)" }
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/auth/me -Headers $headers
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/content -Headers $headers
```

Use `POST /api/v1/auth/login` with the same JSON fields to sign in. All content
and calendar endpoints require `Authorization: Bearer <access_token>`. Each
account can only list or manage its own posts. Existing pre-authentication rows
are kept during migration but remain unassigned and are not exposed to new
accounts.

## PostgreSQL and migrations

Use a PostgreSQL connection URL with the psycopg driver, for example:

```dotenv
DATABASE_URL=postgresql+psycopg://solo_social:change-me@localhost:5432/solo_social
APP_SECRET_KEY=replace-with-a-random-secret-of-at-least-32-characters
APP_ENV=production
APP_AUTO_MIGRATE=false
```

Generate a secret with `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
Apply schema changes as a deployment step before starting the API:

```powershell
python -m alembic upgrade head
```

Production mode requires `APP_SECRET_KEY` and requires automatic startup
migrations to be disabled. Back up the database before applying migrations.

## Try the solo-founder demo

1. Open <http://127.0.0.1:8000/> after starting the app.
2. In **Draft a social post**, use the prefilled bookkeeping-app example or enter
   your own idea, choose a platform, and select **Generate a draft**.
3. In **Plan your week**, enter a theme and start date, then select **Build my
   7-day plan**.
4. See saved drafts and calendar ideas appear below. The **Local demo mode**
   uses a deterministic sample-writing template and does not send prompts to an
   external AI service.

The demo dashboard uses the same content and calendar APIs as the REST interface.
It saves data in the configured SQLite database; remove only that database file
if you want to reset the demo data.

## Optional Gemini generation

To generate captions with Gemini, set the following in `.env`:

```dotenv
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key
GEMINI_MODEL=gemini-2.5-flash
```

The Gemini key is required only when `AI_PROVIDER=gemini`. The default
`AI_PROVIDER=local` makes no external AI requests. To use OpenAI instead, set:

```dotenv
AI_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4o-mini
```

Keep `.env` private; it is ignored by Git. The `LIVEKIT_URL`,
`LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` entries in `.env.example` are
configuration placeholders only. LiveKit voice, room, and token features are
not implemented.

## API overview

All application endpoints are under `/api/v1`.

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/auth/register` | Create an account and return an access token |
| `POST` | `/auth/login` | Sign in and return an access token |
| `GET` | `/auth/me` | Get the authenticated account |
| `POST` | `/content` | Save a content draft |
| `POST` | `/content/generate` | Generate and save a caption |
| `GET` | `/content` | List drafts; optional `platform`, `limit`, and `offset` |
| `GET` | `/content/{id}` | Get a draft |
| `PATCH` | `/content/{id}` | Update a draft |
| `DELETE` | `/content/{id}` | Delete a draft |
| `POST` | `/calendar` | Add one dated calendar post |
| `POST` | `/calendar/weekly` | Create and save a seven-day plan |
| `GET` | `/calendar` | List posts; optional date range, status, `limit`, and `offset` |
| `GET` | `/calendar/{id}` | Get a calendar post |
| `PATCH` | `/calendar/{id}` | Update a calendar post |
| `DELETE` | `/calendar/{id}` | Delete a calendar post |

Example authenticated requests:

```powershell
$headers = @{ Authorization = "Bearer $($account.access_token)" }
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/content/generate `
  -ContentType "application/json" `
  -Headers $headers `
  -Body '{"topic":"Building an audience","platform":"linkedin"}'

Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/calendar/weekly `
  -ContentType "application/json" `
  -Headers $headers `
  -Body '{"topic":"Content strategy","start_date":"2026-11-02"}'
```

Supported platforms are `linkedin`, `x`, and `instagram`. Calendar post statuses
are `planned`, `draft`, `approved`, and `published`. The `published` status is
for tracking only; it does not publish to a social network.

Calendar post `date` and `suggested_time` are planning metadata; no background
worker publishes posts at that time.

## Tests and database setup

```powershell
python -m pytest -q
python -m alembic upgrade head
```

Tests use isolated temporary SQLite databases. Development applies pending
migrations at startup. Production deployments must run migrations explicitly
before starting the API.

## Docker

Copy `.env.example` to `.env`, then run:

```powershell
docker compose up --build
```

Docker stores SQLite data in a named volume so it persists across container
restarts.

## Development

The API code is under `app/`; the single-page web dashboard is
[`dashboard/index.html`](./dashboard/index.html). Supporting modules live in
`ai/`, `automation/`, and `database/`.

Project direction and deferred production features are tracked in
[`docs/project_plan.md`](./docs/project_plan.md).
