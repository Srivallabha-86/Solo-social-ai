from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.routes.auth import router as auth_router
from app.api.routes.calendar import router as calendar_router
from app.api.routes.content import router as content_router
from app.api.routes.health import router as health_router
from app.core.config import settings
from app.db.session import init_db


def create_app(initialize_database: bool = True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        if (
            settings.app_env.lower() in {"prod", "production"}
            and settings.app_auto_migrate
        ):
            raise RuntimeError(
                "Set APP_AUTO_MIGRATE=false in production and run "
                "'alembic upgrade head' as a deployment step."
            )
        if initialize_database and settings.app_auto_migrate:
            init_db()
        yield

    if settings.app_env.lower() in {"prod", "production"}:
        if len(settings.app_secret_key) < 32:
            raise RuntimeError("APP_SECRET_KEY must contain at least 32 characters in production.")

    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="AI-powered weekly social media marketing assistant for solo founders.",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health_router)
    application.include_router(auth_router, prefix="/api/v1")
    application.include_router(content_router, prefix="/api/v1")
    application.include_router(calendar_router, prefix="/api/v1")

    @application.get("/")
    async def root() -> FileResponse:
        page = Path(__file__).resolve().parent.parent / "dashboard" / "index.html"
        return FileResponse(page, media_type="text/html")

    return application


app = create_app()
