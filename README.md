# Solo Social AI

Solo Social AI is a backend MVP for planning a week of social content, drafting
platform-specific captions, and managing saved content and calendar posts.

## Features

- FastAPI endpoints for health checks, content ideas, and calendar posts.
- Local caption generation by default; optional OpenAI generation via environment
  configuration.
- SQLite persistence for saved drafts and calendar plans.
- Content and calendar listing, filtering, updates, and deletion.
- Request validation and automated API/service tests.

Live social publishing, user authentication, database migrations, and background
scheduling are not part of this MVP.

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

Open the interactive API docs at <http://127.0.0.1:8000/docs>. The health check
is available at <http://127.0.0.1:8000/health>.

By default, the app uses local generation and creates `solo_social_ai.db` in the
working directory. No API key is required for local generation.

## Optional OpenAI generation

Set the following in `.env` to use OpenAI for generated captions:

```dotenv
AI_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4o-mini
```

Keep `.env` private; it is ignored by Git. Setting `AI_PROVIDER=local` restores
local generation without making external API calls.

## API overview

All application endpoints are under `/api/v1`.

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/content` | Save a content draft |
| `POST` | `/content/generate` | Generate and save a caption |
| `GET` | `/content` | List drafts; optional `platform`, `limit`, and `offset` |
| `GET` | `/content/{id}` | Get a draft |
| `PATCH` | `/content/{id}` | Update a draft |
| `DELETE` | `/content/{id}` | Delete a draft |
| `POST` | `/calendar/weekly` | Create and save a seven-day plan |
| `GET` | `/calendar` | List posts; optional date range, status, `limit`, and `offset` |
| `GET` | `/calendar/{id}` | Get a calendar post |
| `PATCH` | `/calendar/{id}` | Update a calendar post |
| `DELETE` | `/calendar/{id}` | Delete a calendar post |

Example requests:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/content/generate `
  -ContentType "application/json" `
  -Body '{"topic":"Building an audience","platform":"linkedin"}'

Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/calendar/weekly `
  -ContentType "application/json" `
  -Body '{"topic":"Content strategy","start_date":"2026-11-02"}'
```

Supported platforms are `linkedin`, `x`, and `instagram`. Calendar post statuses
are `planned`, `draft`, `approved`, and `published`. The `published` status is
for tracking only; it does not publish to a social network.

## Tests and database setup

```powershell
python -m pytest -q
python -m scripts.init_db
```

Tests use a temporary SQLite database. The application creates missing tables
when it starts. This MVP does not include schema migrations; back up the
database before upgrading to a version that changes its models.

## Docker

Copy `.env.example` to `.env`, then run:

```powershell
docker compose up --build
```

Docker stores SQLite data in a named volume so it persists across container
restarts.

## Development

The application code is under `app/`; `ai/`, `automation/`, `dashboard/`, and
`database/` contain supporting prototype modules. The documented FastAPI
service is the supported application entry point.

Project direction and deferred production features are tracked in
[`docs/project_plan.md`](./docs/project_plan.md).
